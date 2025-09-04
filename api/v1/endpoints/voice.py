"""
Voice calling API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, Dict, Any
import structlog

from core.database import get_db
from core.security import get_current_user
from models.user import User
from models.candidate import Candidate
from models.interview import Interview
from services.voice_service import VoiceService, VoiceProvider, call_candidate_for_interview, call_candidate_for_offer
from schemas.voice import VoiceCallRequest, VoiceCallResponse, CallStatusResponse

logger = structlog.get_logger()
router = APIRouter()

@router.post("/call", response_model=VoiceCallResponse)
async def make_voice_call(
    request: VoiceCallRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Make a voice call to a phone number
    """
    try:
        voice_service = VoiceService()
        
        # Make the call
        result = await voice_service.make_call(
            to_number=request.to_number,
            message=request.message,
            candidate_id=request.candidate_id,
            interview_id=request.interview_id,
            provider=request.provider
        )
        
        if result["success"]:
            return VoiceCallResponse(
                success=True,
                call_id=result["call_id"],
                status=result["status"],
                provider=result["provider"],
                cost_estimate=result.get("cost_estimate", "Unknown"),
                message="Call initiated successfully"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to make call: {result.get('error', 'Unknown error')}"
            )
            
    except Exception as e:
        logger.error("Voice call failed", error=str(e), user_id=current_user.id)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/call/interview/{interview_id}")
async def call_candidate_for_interview_endpoint(
    interview_id: str,
    custom_message: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Make a voice call to candidate about upcoming interview
    """
    try:
        # Get interview and candidate
        interview = await db.get(Interview, interview_id)
        if not interview:
            raise HTTPException(status_code=404, detail="Interview not found")
            
        candidate = await db.get(Candidate, interview.candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Make the call
        result = await call_candidate_for_interview(
            candidate=candidate,
            interview=interview,
            custom_message=custom_message
        )
        
        if result["success"]:
            return {
                "success": True,
                "call_id": result["call_id"],
                "message": f"Interview reminder call initiated to {candidate.name}",
                "provider": result["provider"],
                "cost_estimate": result.get("cost_estimate")
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to make interview call: {result.get('error')}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Interview call failed", error=str(e), interview_id=interview_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/call/offer/{candidate_id}")
async def call_candidate_for_offer_endpoint(
    candidate_id: str,
    custom_message: Optional[str] = None,
    background_tasks: BackgroundTasks = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Make a voice call to candidate about job offer
    """
    try:
        # Get candidate
        candidate = await db.get(Candidate, candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Make the call
        result = await call_candidate_for_offer(
            candidate=candidate,
            custom_message=custom_message
        )
        
        if result["success"]:
            return {
                "success": True,
                "call_id": result["call_id"],
                "message": f"Offer call initiated to {candidate.name}",
                "provider": result["provider"],
                "cost_estimate": result.get("cost_estimate")
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to make offer call: {result.get('error')}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Offer call failed", error=str(e), candidate_id=candidate_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/call/{call_id}/status", response_model=CallStatusResponse)
async def get_call_status(
    call_id: str,
    provider: VoiceProvider,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the status of a voice call
    """
    try:
        voice_service = VoiceService()
        status = await voice_service.get_call_status(call_id, provider)
        
        return CallStatusResponse(
            call_id=call_id,
            status=status["status"],
            duration=status.get("duration", 0),
            cost=status.get("cost", "0"),
            start_time=status.get("start_time"),
            end_time=status.get("end_time"),
            provider=provider
        )
        
    except Exception as e:
        logger.error("Failed to get call status", error=str(e), call_id=call_id)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def get_voice_providers(
    current_user: User = Depends(get_current_user)
):
    """
    Get available voice providers and their pricing
    """
    return {
        "providers": [
            {
                "name": "Exotel",
                "code": "exotel",
                "cost_per_minute": "₹0.30-0.50",
                "features": ["Indian numbers", "Call recording", "IVR", "Analytics"],
                "recommended": True
            },
            {
                "name": "Knowlarity", 
                "code": "knowlarity",
                "cost_per_minute": "₹0.25-0.45",
                "features": ["Virtual numbers", "Call tracking", "CRM integration"],
                "recommended": True
            },
            {
                "name": "Plivo",
                "code": "plivo", 
                "cost_per_minute": "₹0.35-0.60",
                "features": ["Similar to Twilio", "Indian operations"],
                "recommended": False
            },
            {
                "name": "Twilio",
                "code": "twilio",
                "cost_per_minute": "₹2.50+",
                "features": ["International provider", "Fallback only"],
                "recommended": False
            }
        ],
        "default_provider": "exotel"
    }

# Webhook endpoints for call status updates
@router.post("/webhooks/exotel/status")
async def exotel_webhook(request: dict):
    """Handle Exotel call status webhooks"""
    logger.info("Exotel webhook received", data=request)
    # Process webhook data and update call status in database
    return {"status": "received"}

@router.post("/webhooks/knowlarity/status") 
async def knowlarity_webhook(request: dict):
    """Handle Knowlarity call status webhooks"""
    logger.info("Knowlarity webhook received", data=request)
    return {"status": "received"}

@router.post("/webhooks/plivo/status")
async def plivo_webhook(request: dict):
    """Handle Plivo call status webhooks"""
    logger.info("Plivo webhook received", data=request)
    return {"status": "received"}
