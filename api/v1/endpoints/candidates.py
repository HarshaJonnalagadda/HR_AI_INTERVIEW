from fastapi import APIRouter, Depends, HTTPException, status, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from core.database import get_db
from core.security import get_current_user_id
from models.candidate import Candidate
from models.job import Job
from services.ai_service import AIService
from services.outreach_service import OutreachService
from schemas.candidate import CandidateCreate, CandidateUpdate, CandidateResponse, CandidateBulkApprove
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[CandidateResponse])
async def get_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    job_id: Optional[int] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get all candidates with filtering and pagination"""
    
    query = select(Candidate)
    
    if status:
        query = query.where(Candidate.status == status)
    if job_id:
        query = query.where(Candidate.job_id == job_id)
    
    query = query.offset(skip).limit(limit).order_by(Candidate.created_at.desc())
    
    result = await db.execute(query)
    candidates = result.scalars().all()
    
    return [CandidateResponse(**candidate.to_dict()) for candidate in candidates]

@router.post("/", response_model=CandidateResponse)
async def create_candidate(
    candidate_data: CandidateCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a new candidate with AI analysis"""
    
    # Verify job exists
    job_result = await db.execute(select(Job).where(Job.id == candidate_data.job_id))
    job = job_result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Check if candidate already exists for this job
    existing_result = await db.execute(
        select(Candidate).where(
            Candidate.email == candidate_data.email,
            Candidate.job_id == candidate_data.job_id
        )
    )
    existing = existing_result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidate already exists for this job"
        )
    
    try:
        # Create candidate
        candidate = Candidate(**candidate_data.dict())
        
        # AI Analysis if profile data available
        if candidate.linkedin_url or candidate.resume_url:
            ai_service = AIService()
            analysis = await ai_service.analyze_candidate_match(
                candidate_profile=candidate.to_dict(),
                job_requirements=job.to_dict()
            )
            
            candidate.ai_confidence_score = analysis.get('confidence_score', 0.0)
            candidate.matching_rationale = analysis.get('rationale', '')
        
        db.add(candidate)
        await db.commit()
        await db.refresh(candidate)
        
        return CandidateResponse(**candidate.to_dict())
        
    except Exception as e:
        logger.error(f"Candidate creation error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create candidate"
        )

@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific candidate by ID"""
    
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    return CandidateResponse(**candidate.to_dict())

@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: int,
    candidate_update: CandidateUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Update a candidate"""
    
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    try:
        # Update candidate fields
        update_data = candidate_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'skills':
                candidate.skills_list = value
            else:
                setattr(candidate, field, value)
        
        await db.commit()
        await db.refresh(candidate)
        
        return CandidateResponse(**candidate.to_dict())
        
    except Exception as e:
        logger.error(f"Candidate update error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update candidate"
        )

@router.post("/bulk-approve")
async def bulk_approve_candidates(
    bulk_approve: CandidateBulkApprove,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Approve multiple candidates for outreach"""
    
    result = await db.execute(
        select(Candidate).where(Candidate.id.in_(bulk_approve.candidate_ids))
    )
    candidates = result.scalars().all()
    
    if len(candidates) != len(bulk_approve.candidate_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Some candidates not found"
        )
    
    try:
        results = []
        
        for candidate in candidates:
            if candidate.status == 'sourced':
                candidate.status = 'approved'
                
                # Schedule outreach in background
                background_tasks.add_task(
                    initiate_candidate_outreach,
                    candidate.id,
                    db
                )
                
                results.append({
                    'candidate_id': candidate.id,
                    'status': 'approved',
                    'outreach_scheduled': True
                })
            else:
                results.append({
                    'candidate_id': candidate.id,
                    'status': 'skipped',
                    'reason': f'Current status: {candidate.status}'
                })
        
        await db.commit()
        
        return {
            'message': 'Bulk approval completed',
            'results': results
        }
        
    except Exception as e:
        logger.error(f"Bulk approval error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to approve candidates"
        )

async def initiate_candidate_outreach(candidate_id: int, db: AsyncSession):
    """Background task to initiate outreach for approved candidate"""
    try:
        result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
        candidate = result.scalar_one_or_none()
        
        if candidate:
            outreach_service = OutreachService()
            await outreach_service.send_initial_outreach(candidate)
            
            candidate.status = 'contacted'
            candidate.last_contacted_at = func.now()
            await db.commit()
            
            logger.info(f"Initiated outreach for candidate {candidate_id}")
    except Exception as e:
        logger.error(f"Outreach initiation error: {e}")

@router.get("/{candidate_id}/outreach-history")
async def get_candidate_outreach_history(
    candidate_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get outreach history for a candidate"""
    
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()
    
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )
    
    # Get outreach history (this would be from outreach table)
    # For now, return basic info
    return {
        'candidate_id': candidate_id,
        'outreach_history': [],  # TODO: Implement outreach history
        'last_contacted': candidate.last_contacted_at
    }
