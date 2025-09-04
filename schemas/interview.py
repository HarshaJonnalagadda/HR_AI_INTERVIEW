from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class InterviewBase(BaseModel):
    title: str
    interview_type: str = "technical"
    duration_minutes: int = 60
    timezone: str = "Asia/Kolkata"

class InterviewCreate(InterviewBase):
    candidate_id: int
    interviewer_id: int

class InterviewScheduleRequest(BaseModel):
    candidate_id: int
    interviewer_id: int
    interview_type: str = "technical"
    duration_minutes: int = 60
    timezone: str = "Asia/Kolkata"
    preferred_times: Optional[List[datetime]] = None

class InterviewUpdate(BaseModel):
    title: Optional[str] = None
    interview_type: Optional[str] = None
    duration_minutes: Optional[int] = None
    status: Optional[str] = None
    meeting_link: Optional[str] = None
    reschedule_reason: Optional[str] = None

class InterviewResponse(InterviewBase):
    id: int
    candidate_id: int
    interviewer_id: int
    job_id: int
    scheduled_at: Optional[datetime] = None
    status: str
    meeting_link: Optional[str] = None
    meeting_platform: str
    interviewer_approved: bool
    candidate_confirmed: bool
    approved_slots: Optional[List[str]] = None
    reminder_24h_sent: bool
    reminder_1h_sent: bool
    reschedule_count: int
    reschedule_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
