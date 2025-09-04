from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any

from core.database import get_db
from core.security import get_current_user_id
from models.job import Job
from models.candidate import Candidate
from services.brightdata_service import BrightDataService
from services.ai_service import AIService
from schemas.sourcing import SourcingRequest, SourcingResponse, CandidateMatch
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/search-candidates", response_model=SourcingResponse)
async def search_candidates(
    sourcing_request: SourcingRequest,
    background_tasks: BackgroundTasks,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Search for candidates using BrightData LinkedIn scraper"""
    
    # Verify job exists and user has access
    result = await db.execute(
        select(Job).where(Job.id == sourcing_request.job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    try:
        # Initialize AI service for job analysis
        ai_service = AIService()
        
        # Analyze job if not already done
        if not job.parsed_skills or not job.matching_keywords:
            job_analysis = await ai_service.analyze_job_description(
                job.description, 
                job.requirements or ""
            )
            
            job.parsed_skills_list = job_analysis.get('skills', [])
            job.matching_keywords_list = job_analysis.get('keywords', [])
            job.ai_confidence_score = job_analysis.get('confidence_score', 0.0)
            
            await db.commit()
        
        # Search candidates using BrightData
        async with BrightDataService() as brightdata:
            profiles = await brightdata.search_by_job_requirements(
                job_title=job.title,
                required_skills=job.parsed_skills_list[:5],  # Top 5 skills
                location=sourcing_request.location or job.location or "India",
                experience_level=job.experience_level,
                limit=sourcing_request.limit or 50
            )
        
        # Process and match candidates
        candidate_matches = []
        for profile in profiles:
            # AI matching analysis
            match_analysis = await ai_service.analyze_candidate_match(
                candidate_profile=profile,
                job_requirements=job.to_dict()
            )
            
            candidate_match = CandidateMatch(
                profile_data=profile,
                confidence_score=match_analysis.get('confidence_score', 0.0),
                matching_rationale=match_analysis.get('rationale', ''),
                strengths=match_analysis.get('strengths', []),
                concerns=match_analysis.get('concerns', []),
                recommendation=match_analysis.get('recommendation', 'maybe')
            )
            
            candidate_matches.append(candidate_match)
        
        # Sort by confidence score
        candidate_matches.sort(key=lambda x: x.confidence_score, reverse=True)
        
        # Schedule background task to save high-confidence candidates
        background_tasks.add_task(
            save_promising_candidates,
            candidate_matches[:20],  # Top 20 candidates
            job.id,
            db
        )
        
        return SourcingResponse(
            job_id=job.id,
            job_title=job.title,
            total_found=len(candidate_matches),
            candidates=candidate_matches,
            search_parameters={
                "keywords": job.matching_keywords_list,
                "location": sourcing_request.location or job.location,
                "experience_level": job.experience_level
            }
        )
        
    except Exception as e:
        logger.error(f"Candidate sourcing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search candidates"
        )

async def save_promising_candidates(
    candidate_matches: List[CandidateMatch],
    job_id: int,
    db: AsyncSession
):
    """Background task to save high-confidence candidates to database"""
    
    try:
        for match in candidate_matches:
            if match.confidence_score >= 0.7:  # Only save high-confidence matches
                profile = match.profile_data
                
                # Check if candidate already exists
                result = await db.execute(
                    select(Candidate).where(
                        Candidate.email == profile.get('email', ''),
                        Candidate.job_id == job_id
                    )
                )
                existing = result.scalar_one_or_none()
                
                if not existing and profile.get('email'):
                    candidate = Candidate(
                        first_name=profile.get('first_name', ''),
                        last_name=profile.get('last_name', ''),
                        email=profile.get('email', ''),
                        linkedin_url=profile.get('linkedin_url', ''),
                        current_title=profile.get('current_title', ''),
                        current_company=profile.get('current_company', ''),
                        experience_years=profile.get('experience_years'),
                        location=profile.get('location', ''),
                        skills_list=profile.get('skills', []),
                        ai_confidence_score=match.confidence_score,
                        matching_rationale=match.matching_rationale,
                        source='brightdata_linkedin',
                        status='sourced',
                        job_id=job_id
                    )
                    
                    db.add(candidate)
        
        await db.commit()
        logger.info(f"Saved promising candidates for job {job_id}")
        
    except Exception as e:
        logger.error(f"Error saving candidates: {e}")
        await db.rollback()

@router.get("/jobs/{job_id}/sourcing-status")
async def get_sourcing_status(
    job_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db)
):
    """Get sourcing status for a job"""
    
    result = await db.execute(
        select(Job).where(Job.id == job_id)
    )
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Count candidates by status
    candidates_result = await db.execute(
        select(Candidate).where(Candidate.job_id == job_id)
    )
    candidates = candidates_result.scalars().all()
    
    status_counts = {}
    for candidate in candidates:
        status_counts[candidate.status] = status_counts.get(candidate.status, 0) + 1
    
    return {
        "job_id": job_id,
        "job_title": job.title,
        "total_candidates": len(candidates),
        "status_breakdown": status_counts,
        "ai_analysis_complete": bool(job.parsed_skills and job.matching_keywords),
        "last_sourcing_run": job.updated_at
    }
