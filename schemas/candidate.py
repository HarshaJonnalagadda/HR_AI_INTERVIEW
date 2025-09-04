from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    preferred_contact_method: str = "email"
    timezone: Optional[str] = None

class CandidateCreate(CandidateBase):
    job_id: int
    skills: Optional[List[str]] = None
    source: str = "manual"

class CandidateUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    linkedin_url: Optional[str] = None
    resume_url: Optional[str] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    experience_years: Optional[int] = None
    location: Optional[str] = None
    skills: Optional[List[str]] = None
    status: Optional[str] = None
    preferred_contact_method: Optional[str] = None
    timezone: Optional[str] = None
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    notice_period_days: Optional[int] = None

class CandidateResponse(CandidateBase):
    id: int
    job_id: int
    skills: Optional[List[str]] = None
    ai_confidence_score: Optional[float] = None
    matching_rationale: Optional[str] = None
    status: str
    source: str
    expected_salary_min: Optional[int] = None
    expected_salary_max: Optional[int] = None
    notice_period_days: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    last_contacted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CandidateBulkApprove(BaseModel):
    candidate_ids: List[int]
