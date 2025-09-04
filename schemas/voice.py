"""
Pydantic schemas for voice calling API
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from services.voice_service import VoiceProvider, CallStatus

class VoiceCallRequest(BaseModel):
    """Request schema for making a voice call"""
    to_number: str = Field(..., description="Phone number to call (Indian format preferred)")
    message: str = Field(..., description="Message to convert to speech")
    candidate_id: Optional[str] = Field(None, description="Candidate ID for tracking")
    interview_id: Optional[str] = Field(None, description="Interview ID for tracking")
    provider: Optional[VoiceProvider] = Field(None, description="Specific provider to use")
    
    class Config:
        schema_extra = {
            "example": {
                "to_number": "+919876543210",
                "message": "Hello, this is a reminder about your interview tomorrow at 2 PM. Please confirm your availability.",
                "candidate_id": "123e4567-e89b-12d3-a456-426614174000",
                "provider": "exotel"
            }
        }

class VoiceCallResponse(BaseModel):
    """Response schema for voice call initiation"""
    success: bool
    call_id: str
    status: CallStatus
    provider: VoiceProvider
    cost_estimate: str
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "call_id": "exo_call_123456",
                "status": "initiated",
                "provider": "exotel",
                "cost_estimate": "₹0.40/min",
                "message": "Call initiated successfully"
            }
        }

class CallStatusResponse(BaseModel):
    """Response schema for call status"""
    call_id: str
    status: CallStatus
    duration: int = Field(0, description="Call duration in seconds")
    cost: str = Field("0", description="Call cost")
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    provider: VoiceProvider
    
    class Config:
        schema_extra = {
            "example": {
                "call_id": "exo_call_123456",
                "status": "completed",
                "duration": 45,
                "cost": "₹0.30",
                "start_time": "2024-01-15T14:30:00Z",
                "end_time": "2024-01-15T14:30:45Z",
                "provider": "exotel"
            }
        }

class InterviewCallRequest(BaseModel):
    """Request schema for interview reminder call"""
    interview_id: str
    custom_message: Optional[str] = Field(None, description="Custom message override")
    
class OfferCallRequest(BaseModel):
    """Request schema for offer call"""
    candidate_id: str
    custom_message: Optional[str] = Field(None, description="Custom message override")
