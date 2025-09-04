from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SourcingRequest(BaseModel):
    job_id: int
    location: Optional[str] = None
    limit: Optional[int] = 50
    experience_level: Optional[str] = None

class CandidateMatch(BaseModel):
    profile_data: Dict[str, Any]
    confidence_score: float
    matching_rationale: str
    strengths: List[str]
    concerns: List[str]
    recommendation: str

class SourcingResponse(BaseModel):
    job_id: int
    job_title: str
    total_found: int
    candidates: List[CandidateMatch]
    search_parameters: Dict[str, Any]
