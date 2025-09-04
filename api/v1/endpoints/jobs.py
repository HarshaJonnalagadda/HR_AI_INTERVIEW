from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional

from core.database import get_db
from core.security import get_current_user_id
from models.job import Job
from models.candidate import Candidate
from models.negotiation import Negotiation
from services.ai_service import AIService
from schemas.job import JobCreate, JobUpdate, JobResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[JobResponse])
async def get_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get all jobs with filtering and pagination"""
    
    query = select(Job)
    
    if status:
        query = query.where(Job.status == status)
    if department:
        query = query.where(Job.department == department)
    
    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    
    result = await db.execute(query)
    jobs = result.scalars().all()
    
    # Get candidate counts for each job
    job_responses = []
    for job in jobs:
        candidate_count_result = await db.execute(
            select(func.count(Candidate.id)).where(Candidate.job_id == job.id)
        )
        candidate_count = candidate_count_result.scalar()
        
        job_dict = job.to_dict()
        job_dict['candidate_count'] = candidate_count
        job_responses.append(JobResponse(**job_dict))
    
    return job_responses

@router.post("/", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Create a new job posting with AI analysis"""
    
    try:
        # Create job instance
        job = Job(
            **job_data.dict(),
            created_by=current_user_id
        )
        
        # AI Analysis of Job Description
        ai_service = AIService()
        analysis = await ai_service.analyze_job_description(
            job_data.description, 
            job_data.requirements or ""
        )
        
        job.parsed_skills_list = analysis.get('skills', [])
        job.ai_confidence_score = analysis.get('confidence_score', 0.0)
        job.matching_keywords_list = analysis.get('keywords', [])
        
        db.add(job)
        await db.commit()
        await db.refresh(job)
        
        job_dict = job.to_dict()
        job_dict['candidate_count'] = 0
        
        return JobResponse(**job_dict)
        
    except Exception as e:
        logger.error(f"Job creation error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create job"
        )

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific job by ID"""
    
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Get candidate count
    candidate_count_result = await db.execute(
        select(func.count(Candidate.id)).where(Candidate.job_id == job_id)
    )
    candidate_count = candidate_count_result.scalar()
    
    job_dict = job.to_dict()
    job_dict['candidate_count'] = candidate_count
    
    return JobResponse(**job_dict)

@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_update: JobUpdate,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Update a job posting"""
    
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    try:
        # Update job fields
        update_data = job_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(job, field, value)
        
        # Re-analyze if description or requirements changed
        if 'description' in update_data or 'requirements' in update_data:
            ai_service = AIService()
            analysis = await ai_service.analyze_job_description(
                job.description, 
                job.requirements or ""
            )
            
            job.parsed_skills_list = analysis.get('skills', [])
            job.ai_confidence_score = analysis.get('confidence_score', 0.0)
            job.matching_keywords_list = analysis.get('keywords', [])
        
        await db.commit()
        await db.refresh(job)
        
        # Get candidate count
        candidate_count_result = await db.execute(
            select(func.count(Candidate.id)).where(Candidate.job_id == job_id)
        )
        candidate_count = candidate_count_result.scalar()
        
        job_dict = job.to_dict()
        job_dict['candidate_count'] = candidate_count
        
        return JobResponse(**job_dict)
        
    except Exception as e:
        logger.error(f"Job update error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update job"
        )

@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Delete a job posting"""
    
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    try:
        await db.delete(job)
        await db.commit()
        
        return {"message": "Job deleted successfully"}
        
    except Exception as e:
        logger.error(f"Job deletion error: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job"
        )
