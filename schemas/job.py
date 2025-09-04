from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class JobBase(BaseModel):
    title: str
    description: str
    requirements: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: str = "full-time"
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: str = "INR"
    priority: str = "medium"

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None

class JobResponse(JobBase):
    id: int
    status: str
    parsed_skills: Optional[List[str]] = None
    ai_confidence_score: Optional[float] = None
    matching_keywords: Optional[List[str]] = None
    created_by: int
    created_at: datetime
    updated_at: datetime
    deadline: Optional[datetime] = None
    candidate_count: int = 0

    class Config:
        from_attributes = True
