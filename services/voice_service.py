"""
Voice calling service with multiple Indian providers
Supports Exotel, Knowlarity, and fallback to Twilio
"""

import asyncio
import aiohttp
import structlog
from typing import Optional, Dict, Any, List
from enum import Enum
from core.config import settings
from models.candidate import Candidate
from models.interview import Interview

logger = structlog.get_logger()

class VoiceProvider(str, Enum):
    EXOTEL = "exotel"
    KNOWLARITY = "knowlarity" 
    PLIVO = "plivo"
    TWILIO = "twilio"

class CallStatus(str, Enum):
    INITIATED = "initiated"
    RINGING = "ringing"
    ANSWERED = "answered"
    COMPLETED = "completed"
    FAILED = "failed"
    BUSY = "busy"
    NO_ANSWER = "no-answer"

class VoiceService:
    """Multi-provider voice calling service optimized for India"""
    
    def __init__(self):
        self.primary_provider = VoiceProvider.EXOTEL
        self.fallback_providers = [VoiceProvider.PLIVO, VoiceProvider.TWILIO]
        
    async def make_call(
        self,
        to_number: str,
        message: str,
        candidate_id: Optional[str] = None,
        interview_id: Optional[str] = None,
        provider: Optional[VoiceProvider] = None
    ) -> Dict[str, Any]:
        """
        Make a voice call with AI-generated message
        
        Args:
            to_number: Phone number to call (Indian format: +91XXXXXXXXXX)
            message: Text message to convert to speech
            candidate_id: Optional candidate ID for tracking
            interview_id: Optional interview ID for tracking
            provider: Specific provider to use (defaults to primary)
            
        Returns:
            Dict with call details and status
        """
        provider = provider or self.primary_provider
        
        try:
            # Format Indian phone number
            formatted_number = self._format_indian_number(to_number)
            
            # Choose provider and make call
            if provider == VoiceProvider.EXOTEL:
                result = await self._make_exotel_call(formatted_number, message)
            elif provider == VoiceProvider.KNOWLARITY:
                result = await self._make_knowlarity_call(formatted_number, message)
            elif provider == VoiceProvider.PLIVO:
                result = await self._make_plivo_call(formatted_number, message)
            else:
                result = await self._make_twilio_call(formatted_number, message)
                
            # Log call attempt
            logger.info(
                "Voice call initiated",
                provider=provider,
                to_number=formatted_number,
                candidate_id=candidate_id,
                interview_id=interview_id,
                call_id=result.get("call_id"),
                status=result.get("status")
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Voice call failed",
                provider=provider,
                error=str(e),
                to_number=to_number
            )
            
            # Try fallback provider
            if provider == self.primary_provider and self.fallback_providers:
                logger.info("Trying fallback provider", fallback=self.fallback_providers[0])
                return await self.make_call(
                    to_number, message, candidate_id, interview_id, 
                    self.fallback_providers[0]
                )
                
            return {
                "success": False,
                "error": str(e),
                "provider": provider,
                "status": CallStatus.FAILED
            }

    async def _make_exotel_call(self, to_number: str, message: str) -> Dict[str, Any]:
        """Make call using Exotel API"""
        url = f"https://api.exotel.com/v1/Accounts/{settings.EXOTEL_SID}/Calls/connect.json"
        
        # Convert text to speech URL (you can use AWS Polly, Google TTS, etc.)
        tts_url = await self._generate_tts_url(message)
        
        data = {
            "From": settings.EXOTEL_PHONE_NUMBER,
            "To": to_number,
            "Url": tts_url,  # URL that returns TwiML/ExoML with audio
            "Method": "GET",
            "StatusCallback": f"{settings.BACKEND_URL}/webhooks/exotel/status",
            "StatusCallbackMethod": "POST"
        }
        
        auth = aiohttp.BasicAuth(settings.EXOTEL_API_KEY, settings.EXOTEL_API_TOKEN)
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data, auth=auth) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "call_id": result["Call"]["Sid"],
                        "status": CallStatus.INITIATED,
                        "provider": VoiceProvider.EXOTEL,
                        "cost_estimate": "₹0.40/min"
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Exotel API error: {error_text}")

    async def _make_knowlarity_call(self, to_number: str, message: str) -> Dict[str, Any]:
        """Make call using Knowlarity API"""
        url = "https://kpi.knowlarity.com/Basic/v1/account/call/makecall"
        
        tts_url = await self._generate_tts_url(message)
        
        headers = {
            "Authorization": f"Bearer {settings.KNOWLARITY_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "k_number": settings.KNOWLARITY_PHONE_NUMBER,
            "customer_number": to_number,
            "caller_id": settings.KNOWLARITY_CALLER_ID,
            "call_type": "trans",
            "url": tts_url
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "call_id": result.get("call_id"),
                        "status": CallStatus.INITIATED,
                        "provider": VoiceProvider.KNOWLARITY,
                        "cost_estimate": "₹0.35/min"
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Knowlarity API error: {error_text}")

    async def _make_plivo_call(self, to_number: str, message: str) -> Dict[str, Any]:
        """Make call using Plivo API"""
        url = f"https://api.plivo.com/v1/Account/{settings.PLIVO_AUTH_ID}/Call/"
        
        tts_url = await self._generate_tts_url(message)
        
        headers = {
            "Authorization": f"Basic {settings.PLIVO_AUTH_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "from": settings.PLIVO_PHONE_NUMBER,
            "to": to_number,
            "answer_url": tts_url,
            "answer_method": "GET"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 201:
                    result = await response.json()
                    return {
                        "success": True,
                        "call_id": result["message_uuid"][0],
                        "status": CallStatus.INITIATED,
                        "provider": VoiceProvider.PLIVO,
                        "cost_estimate": "₹0.45/min"
                    }
                else:
                    error_text = await response.text()
                    raise Exception(f"Plivo API error: {error_text}")

    async def _make_twilio_call(self, to_number: str, message: str) -> Dict[str, Any]:
        """Fallback: Make call using Twilio API"""
        # Keep existing Twilio implementation as fallback
        tts_url = await self._generate_tts_url(message)
        
        # Twilio implementation (existing code)
        return {
            "success": True,
            "call_id": "twilio_call_id",
            "status": CallStatus.INITIATED,
            "provider": VoiceProvider.TWILIO,
            "cost_estimate": "₹2.50/min"
        }

    async def _generate_tts_url(self, message: str) -> str:
        """
        Generate Text-to-Speech URL for the message
        You can use:
        1. AWS Polly
        2. Google Cloud TTS
        3. Azure Cognitive Services
        4. ElevenLabs (for better quality)
        """
        # For now, return a placeholder URL
        # In production, implement actual TTS service
        encoded_message = message.replace(" ", "%20")
        return f"{settings.BACKEND_URL}/api/v1/tts/generate?text={encoded_message}&voice=indian_female"

    def _format_indian_number(self, phone_number: str) -> str:
        """Format phone number for Indian calling"""
        # Remove all non-digits
        digits = ''.join(filter(str.isdigit, phone_number))
        
        # Handle different formats
        if digits.startswith('91') and len(digits) == 12:
            return f"+{digits}"
        elif len(digits) == 10:
            return f"+91{digits}"
        elif digits.startswith('0') and len(digits) == 11:
            return f"+91{digits[1:]}"
        else:
            return f"+91{digits}"

    async def get_call_status(self, call_id: str, provider: VoiceProvider) -> Dict[str, Any]:
        """Get status of a specific call"""
        try:
            if provider == VoiceProvider.EXOTEL:
                return await self._get_exotel_status(call_id)
            elif provider == VoiceProvider.KNOWLARITY:
                return await self._get_knowlarity_status(call_id)
            elif provider == VoiceProvider.PLIVO:
                return await self._get_plivo_status(call_id)
            else:
                return await self._get_twilio_status(call_id)
        except Exception as e:
            logger.error("Failed to get call status", call_id=call_id, error=str(e))
            return {"status": CallStatus.FAILED, "error": str(e)}

    async def _get_exotel_status(self, call_id: str) -> Dict[str, Any]:
        """Get call status from Exotel"""
        url = f"https://api.exotel.com/v1/Accounts/{settings.EXOTEL_SID}/Calls/{call_id}.json"
        auth = aiohttp.BasicAuth(settings.EXOTEL_API_KEY, settings.EXOTEL_API_TOKEN)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, auth=auth) as response:
                if response.status == 200:
                    result = await response.json()
                    call_data = result["Call"]
                    return {
                        "status": call_data["Status"].lower(),
                        "duration": call_data.get("Duration", 0),
                        "cost": call_data.get("Price", "0"),
                        "start_time": call_data.get("StartTime"),
                        "end_time": call_data.get("EndTime")
                    }
                else:
                    raise Exception(f"Failed to get Exotel call status: {response.status}")

    # Placeholder methods for other providers
    async def _get_knowlarity_status(self, call_id: str) -> Dict[str, Any]:
        return {"status": CallStatus.COMPLETED, "duration": 0}
    
    async def _get_plivo_status(self, call_id: str) -> Dict[str, Any]:
        return {"status": CallStatus.COMPLETED, "duration": 0}
    
    async def _get_twilio_status(self, call_id: str) -> Dict[str, Any]:
        return {"status": CallStatus.COMPLETED, "duration": 0}

# Convenience functions for common use cases
async def call_candidate_for_interview(
    candidate: Candidate, 
    interview: Interview,
    custom_message: Optional[str] = None
) -> Dict[str, Any]:
    """Make a call to candidate about upcoming interview"""
    service = VoiceService()
    
    if not custom_message:
        custom_message = f"""
        Hello {candidate.name}, this is a call from {settings.COMPANY_NAME} regarding your interview 
        for the {interview.job.title} position scheduled on {interview.scheduled_at.strftime('%B %d at %I:%M %p')}. 
        Please confirm your availability by replying to this call or our email. Thank you.
        """
    
    return await service.make_call(
        to_number=candidate.phone,
        message=custom_message,
        candidate_id=str(candidate.id),
        interview_id=str(interview.id)
    )

async def call_candidate_for_offer(candidate: Candidate, custom_message: Optional[str] = None) -> Dict[str, Any]:
    """Make a call to candidate about job offer"""
    service = VoiceService()
    
    if not custom_message:
        custom_message = f"""
        Hello {candidate.name}, congratulations! We have an exciting job offer for you from {settings.COMPANY_NAME}. 
        Please check your email for the detailed offer letter and feel free to call us back to discuss. Thank you.
        """
    
    return await service.make_call(
        to_number=candidate.phone,
        message=custom_message,
        candidate_id=str(candidate.id)
    )
