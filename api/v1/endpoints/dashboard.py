from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Dict, Any, List
from datetime import datetime, timedelta

from core.database import get_db
from core.security import get_current_user_id
from models.job import Job
from models.candidate import Candidate
from models.interview import Interview
from models.user import User
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard overview with key metrics"""
    
    try:
        # Get current user
        user_result = await db.execute(select(User).where(User.id == current_user_id))
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate date ranges
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Job metrics
        total_jobs_result = await db.execute(select(func.count(Job.id)))
        total_jobs = total_jobs_result.scalar()
        
        active_jobs_result = await db.execute(
            select(func.count(Job.id)).where(Job.status == 'active')
        )
        active_jobs = active_jobs_result.scalar()
        
        # Candidate metrics
        total_candidates_result = await db.execute(select(func.count(Candidate.id)))
        total_candidates = total_candidates_result.scalar()
        
        new_candidates_result = await db.execute(
            select(func.count(Candidate.id)).where(
                func.date(Candidate.created_at) >= week_ago
            )
        )
        new_candidates_this_week = new_candidates_result.scalar()
        
        # Candidate status breakdown
        candidate_status_result = await db.execute(
            select(Candidate.status, func.count(Candidate.id))
            .group_by(Candidate.status)
        )
        candidate_status_breakdown = dict(candidate_status_result.all())
        
        # Interview metrics
        total_interviews_result = await db.execute(select(func.count(Interview.id)))
        total_interviews = total_interviews_result.scalar()
        
        upcoming_interviews_result = await db.execute(
            select(func.count(Interview.id)).where(
                and_(
                    Interview.scheduled_at >= datetime.now(),
                    Interview.status == 'scheduled'
                )
            )
        )
        upcoming_interviews = upcoming_interviews_result.scalar()
        
        # Recent activity
        recent_candidates_result = await db.execute(
            select(Candidate)
            .order_by(Candidate.created_at.desc())
            .limit(5)
        )
        recent_candidates = recent_candidates_result.scalars().all()
        
        recent_interviews_result = await db.execute(
            select(Interview)
            .where(Interview.scheduled_at >= datetime.now())
            .order_by(Interview.scheduled_at.asc())
            .limit(5)
        )
        upcoming_interviews_list = recent_interviews_result.scalars().all()
        
        # Performance metrics
        high_confidence_candidates_result = await db.execute(
            select(func.count(Candidate.id)).where(
                Candidate.ai_confidence_score >= 0.8
            )
        )
        high_confidence_candidates = high_confidence_candidates_result.scalar()
        
        return {
            "user": {
                "name": user.full_name,
                "role": user.role,
                "department": user.department
            },
            "metrics": {
                "jobs": {
                    "total": total_jobs,
                    "active": active_jobs,
                    "draft": total_jobs - active_jobs
                },
                "candidates": {
                    "total": total_candidates,
                    "new_this_week": new_candidates_this_week,
                    "high_confidence": high_confidence_candidates,
                    "status_breakdown": candidate_status_breakdown
                },
                "interviews": {
                    "total": total_interviews,
                    "upcoming": upcoming_interviews
                }
            },
            "recent_activity": {
                "recent_candidates": [
                    {
                        "id": c.id,
                        "name": c.full_name,
                        "job_title": c.job.title if c.job else "Unknown",
                        "confidence_score": c.ai_confidence_score,
                        "status": c.status,
                        "created_at": c.created_at.isoformat()
                    } for c in recent_candidates
                ],
                "upcoming_interviews": [
                    {
                        "id": i.id,
                        "candidate_name": i.candidate.full_name if i.candidate else "Unknown",
                        "job_title": i.job.title if i.job else "Unknown",
                        "scheduled_at": i.scheduled_at.isoformat() if i.scheduled_at else None,
                        "status": i.status,
                        "interviewer": i.interviewer.full_name if i.interviewer else "Unknown"
                    } for i in upcoming_interviews_list
                ]
            }
        }
        
    except Exception as e:
        logger.error(f"Dashboard overview error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dashboard data"
        )

@router.get("/pipeline/{job_id}")
async def get_job_pipeline(
    job_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get detailed pipeline view for a specific job"""
    
    try:
        # Verify job exists
        job_result = await db.execute(select(Job).where(Job.id == job_id))
        job = job_result.scalar_one_or_none()
        
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get candidates by status
        candidates_result = await db.execute(
            select(Candidate).where(Candidate.job_id == job_id)
        )
        candidates = candidates_result.scalars().all()
        
        # Group candidates by status
        pipeline_stages = {
            "sourced": [],
            "approved": [],
            "contacted": [],
            "replied": [],
            "interview_scheduled": [],
            "interviewed": [],
            "offer_pending": [],
            "offer_accepted": [],
            "offer_rejected": [],
            "withdrawn": []
        }
        
        for candidate in candidates:
            if candidate.status in pipeline_stages:
                pipeline_stages[candidate.status].append({
                    "id": candidate.id,
                    "name": candidate.full_name,
                    "email": candidate.email,
                    "confidence_score": candidate.ai_confidence_score,
                    "current_company": candidate.current_company,
                    "experience_years": candidate.experience_years,
                    "last_contacted": candidate.last_contacted_at.isoformat() if candidate.last_contacted_at else None,
                    "created_at": candidate.created_at.isoformat()
                })
        
        # Calculate conversion rates
        total_candidates = len(candidates)
        conversion_rates = {}
        
        if total_candidates > 0:
            for stage, stage_candidates in pipeline_stages.items():
                conversion_rates[stage] = len(stage_candidates) / total_candidates * 100
        
        return {
            "job": {
                "id": job.id,
                "title": job.title,
                "status": job.status,
                "created_at": job.created_at.isoformat()
            },
            "pipeline_stages": pipeline_stages,
            "conversion_rates": conversion_rates,
            "total_candidates": total_candidates
        }
        
    except Exception as e:
        logger.error(f"Job pipeline error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load job pipeline"
        )

@router.get("/analytics")
async def get_analytics(
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get recruitment analytics and insights"""
    
    try:
        # Time-based metrics
        today = datetime.now().date()
        last_30_days = today - timedelta(days=30)
        
        # Sourcing effectiveness
        sourcing_stats_result = await db.execute(
            select(
                Candidate.source,
                func.count(Candidate.id).label('count'),
                func.avg(Candidate.ai_confidence_score).label('avg_confidence')
            )
            .group_by(Candidate.source)
        )
        sourcing_stats = sourcing_stats_result.all()
        
        # Interview success rates
        interview_stats_result = await db.execute(
            select(
                Interview.status,
                func.count(Interview.id).label('count')
            )
            .group_by(Interview.status)
        )
        interview_stats = dict(interview_stats_result.all())
        
        # Time to hire metrics
        hired_candidates_result = await db.execute(
            select(Candidate)
            .where(Candidate.status == 'offer_accepted')
            .where(func.date(Candidate.created_at) >= last_30_days)
        )
        hired_candidates = hired_candidates_result.scalars().all()
        
        avg_time_to_hire = 0
        if hired_candidates:
            total_days = sum([
                (datetime.now().date() - c.created_at.date()).days 
                for c in hired_candidates
            ])
            avg_time_to_hire = total_days / len(hired_candidates)
        
        # AI performance metrics
        ai_accuracy_result = await db.execute(
            select(
                func.avg(Candidate.ai_confidence_score).label('avg_confidence'),
                func.count(Candidate.id).filter(Candidate.ai_confidence_score >= 0.8).label('high_confidence'),
                func.count(Candidate.id).label('total')
            )
        )
        ai_stats = ai_accuracy_result.first()
        
        return {
            "sourcing_effectiveness": [
                {
                    "source": stat.source,
                    "candidate_count": stat.count,
                    "avg_confidence_score": round(stat.avg_confidence or 0, 2)
                } for stat in sourcing_stats
            ],
            "interview_pipeline": interview_stats,
            "performance_metrics": {
                "avg_time_to_hire_days": round(avg_time_to_hire, 1),
                "ai_avg_confidence": round(ai_stats.avg_confidence or 0, 2),
                "high_confidence_rate": round(
                    (ai_stats.high_confidence / ai_stats.total * 100) if ai_stats.total > 0 else 0, 1
                )
            },
            "period": {
                "start_date": last_30_days.isoformat(),
                "end_date": today.isoformat()
            }
        }
        
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load analytics"
        )
