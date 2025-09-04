from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user_id
from models.interview import Interview
from models.candidate import Candidate
from models.user import User
from services.calendar_service import CalendarService
from services.outreach_service import OutreachService
from schemas.interview import InterviewCreate, InterviewUpdate, InterviewResponse, InterviewScheduleRequest
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[InterviewResponse])
async def get_interviews(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    interviewer_id: Optional[int] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get interviews with filtering"""
    
    query = select(Interview)
    
    if status:
        query = query.where(Interview.status == status)
    if interviewer_id:
        query = query.where(Interview.interviewer_id == interviewer_id)
    
    query = query.offset(skip).limit(limit).order_by(Interview.scheduled_at.desc())
    
    result = await db.execute(query)
    interviews = result.scalars().all()
    
    return [InterviewResponse(**interview.to_dict()) for interview in interviews]

@router.post("/schedule", response_model=InterviewResponse)
async def schedule_interview(
    schedule_request: InterviewScheduleRequest,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Schedule an interview with interviewer approval workflow"""
    
    # Verify candidate exists
    candidate_result = await db.execute(
        select(Candidate).where(Candidate.id == schedule_request.candidate_id)
    )
    candidate = candidate_result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Verify interviewer exists
    interviewer_result = await db.execute(
        select(User).where(User.id == schedule_request.interviewer_id)
    )
    interviewer = interviewer_result.scalar_one_or_none()
    
    if not interviewer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interviewer not found"
        )
    
    try:
        # Create interview
        interview = Interview(
            title=f"{schedule_request.interview_type.title()} Interview - {candidate.full_name}",
            interview_type=schedule_request.interview_type,
            candidate_id=schedule_request.candidate_id,
            interviewer_id=schedule_request.interviewer_id,
            job_id=candidate.job_id,
            duration_minutes=schedule_request.duration_minutes,
            timezone=schedule_request.timezone or "Asia/Kolkata",
            status="pending_approval"
        )
        
        # Get suggested time slots using calendar service
        calendar_service = CalendarService()
        suggested_slots = await calendar_service.get_available_slots(
            interviewer_id=schedule_request.interviewer_id,
            duration_minutes=schedule_request.duration_minutes,
            preferred_times=schedule_request.preferred_times
        )
        
        interview.approved_slots_list = suggested_slots
        
        db.add(interview)
        await db.commit()
        await db.refresh(interview)
        
        # Send approval request to interviewer
        background_tasks.add_task(
            send_interviewer_approval_request,
            interview.id,
            interviewer.email,
            db
        )
        
        return InterviewResponse(**interview.to_dict())
        
    except Exception as e:
        logger.error(f"Interview scheduling error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to schedule interview"
        )

@router.post("/{interview_id}/approve-slots")
async def approve_interview_slots(
    interview_id: int,
    approved_slots: List[datetime],
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Interviewer approves available time slots"""
    
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    # Verify current user is the interviewer
    if interview.interviewer_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the assigned interviewer can approve slots"
        )
    
    try:
        interview.approved_slots_list = [slot.isoformat() for slot in approved_slots]
        interview.interviewer_approved = True
        interview.status = "slots_approved"
        
        await db.commit()
        
        # Send scheduling link to candidate
        outreach_service = OutreachService()
        candidate = await db.get(Candidate, interview.candidate_id)
        
        scheduling_link = f"https://your-domain.com/schedule/{interview.id}"
        
        await outreach_service.send_interview_invitation(
            candidate=candidate,
            interview_details={
                "job_title": candidate.job.title,
                "interviewer_name": interview.interviewer.full_name,
                "approved_slots": approved_slots,
                "scheduling_link": scheduling_link,
                "duration_minutes": interview.duration_minutes
            }
        )
        
        return {"message": "Slots approved and candidate notified"}
        
    except Exception as e:
        logger.error(f"Slot approval error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve slots"
        )

@router.post("/{interview_id}/confirm")
async def confirm_interview_time(
    interview_id: int,
    selected_time: datetime,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Candidate confirms interview time"""
    
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    try:
        # Verify selected time is in approved slots
        approved_times = [datetime.fromisoformat(slot) for slot in interview.approved_slots_list]
        if selected_time not in approved_times:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Selected time not in approved slots"
            )
        
        # Update interview
        interview.scheduled_at = selected_time
        interview.candidate_confirmed = True
        interview.status = "scheduled"
        
        # Generate meeting link
        calendar_service = CalendarService()
        meeting_details = await calendar_service.create_meeting(
            title=interview.title,
            start_time=selected_time,
            duration_minutes=interview.duration_minutes,
            attendees=[
                interview.candidate.email,
                interview.interviewer.email
            ]
        )
        
        interview.meeting_link = meeting_details.get('meeting_link')
        interview.meeting_id = meeting_details.get('meeting_id')
        
        await db.commit()
        
        # Schedule reminders
        await schedule_interview_reminders(interview_id, db)
        
        return {
            "message": "Interview confirmed",
            "meeting_link": interview.meeting_link,
            "scheduled_at": interview.scheduled_at
        }
        
    except Exception as e:
        logger.error(f"Interview confirmation error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to confirm interview"
        )

@router.post("/{interview_id}/reschedule")
async def reschedule_interview(
    interview_id: int,
    new_time: datetime,
    reason: Optional[str] = None,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Reschedule an interview"""
    
    result = await db.execute(select(Interview).where(Interview.id == interview_id))
    interview = result.scalar_one_or_none()
    
    if not interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    try:
        # Store original time
        interview.original_scheduled_at = interview.scheduled_at
        interview.scheduled_at = new_time
        interview.reschedule_count += 1
        interview.reschedule_reason = reason
        interview.status = "rescheduled"
        
        # Update meeting
        calendar_service = CalendarService()
        await calendar_service.update_meeting(
            meeting_id=interview.meeting_id,
            new_start_time=new_time,
            duration_minutes=interview.duration_minutes
        )
        
        await db.commit()
        
        # Notify participants
        outreach_service = OutreachService()
        candidate = await db.get(Candidate, interview.candidate_id)
        
        await outreach_service.send_interview_invitation(
            candidate=candidate,
            interview_details={
                "job_title": candidate.job.title,
                "scheduled_at": new_time.isoformat(),
                "meeting_link": interview.meeting_link,
                "duration_minutes": interview.duration_minutes,
                "is_rescheduled": True,
                "reschedule_reason": reason
            }
        )
        
        return {"message": "Interview rescheduled successfully"}
        
    except Exception as e:
        logger.error(f"Interview reschedule error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reschedule interview"
        )

async def send_interviewer_approval_request(
    interview_id: int, 
    interviewer_email: str, 
    db: AsyncSession
):
    """Background task to send approval request to interviewer"""
    try:
        # This would send an email to the interviewer with approval link
        # For now, just log
        logger.info(f"Sent approval request for interview {interview_id} to {interviewer_email}")
    except Exception as e:
        logger.error(f"Failed to send approval request: {e}")

async def schedule_interview_reminders(interview_id: int, db: AsyncSession):
    """Schedule 24h and 1h reminders for interview"""
    try:
        # This would schedule background tasks for reminders
        # For now, just log
        logger.info(f"Scheduled reminders for interview {interview_id}")
    except Exception as e:
        logger.error(f"Failed to schedule reminders: {e}")
