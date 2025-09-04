import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import httpx
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class CalendarService:
    """Calendar integration service for Google Calendar and Microsoft Outlook"""
    
    def __init__(self):
        self.google_scopes = ['https://www.googleapis.com/auth/calendar']
        self.microsoft_scopes = ['https://graph.microsoft.com/calendars.readwrite']
    
    async def get_available_slots(
        self,
        interviewer_id: int,
        duration_minutes: int = 60,
        preferred_times: Optional[List[datetime]] = None,
        days_ahead: int = 14
    ) -> List[str]:
        """Get available time slots for interviewer"""
        
        try:
            # Generate time slots for next 14 days (business hours)
            available_slots = []
            start_date = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            
            for day in range(days_ahead):
                current_date = start_date + timedelta(days=day)
                
                # Skip weekends
                if current_date.weekday() >= 5:
                    continue
                
                # Generate slots from 9 AM to 6 PM
                for hour in range(9, 18):
                    slot_time = current_date.replace(hour=hour, minute=0)
                    
                    # Check if slot has enough duration before end of day
                    if slot_time.hour + (duration_minutes / 60) <= 18:
                        available_slots.append(slot_time.isoformat())
            
            # TODO: Integrate with actual calendar APIs to check availability
            # For now, return generated slots
            return available_slots[:20]  # Return first 20 slots
            
        except Exception as e:
            logger.error(f"Error getting available slots: {e}")
            return []
    
    async def create_meeting(
        self,
        title: str,
        start_time: datetime,
        duration_minutes: int,
        attendees: List[str],
        description: str = ""
    ) -> Dict[str, Any]:
        """Create a meeting and return meeting details"""
        
        try:
            # For now, generate a mock Google Meet link
            # In production, this would integrate with Google Calendar API
            meeting_id = f"meet-{int(start_time.timestamp())}"
            meeting_link = f"https://meet.google.com/{meeting_id}"
            
            meeting_details = {
                'meeting_id': meeting_id,
                'meeting_link': meeting_link,
                'title': title,
                'start_time': start_time.isoformat(),
                'end_time': (start_time + timedelta(minutes=duration_minutes)).isoformat(),
                'attendees': attendees,
                'platform': 'google_meet'
            }
            
            logger.info(f"Created meeting: {meeting_id}")
            return meeting_details
            
        except Exception as e:
            logger.error(f"Error creating meeting: {e}")
            return {
                'meeting_id': None,
                'meeting_link': None,
                'error': str(e)
            }
    
    async def update_meeting(
        self,
        meeting_id: str,
        new_start_time: datetime,
        duration_minutes: int
    ) -> Dict[str, Any]:
        """Update existing meeting time"""
        
        try:
            # Mock update - in production would call calendar API
            logger.info(f"Updated meeting {meeting_id} to {new_start_time}")
            
            return {
                'success': True,
                'meeting_id': meeting_id,
                'new_start_time': new_start_time.isoformat(),
                'new_end_time': (new_start_time + timedelta(minutes=duration_minutes)).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error updating meeting: {e}")
            return {'success': False, 'error': str(e)}
    
    async def cancel_meeting(self, meeting_id: str) -> Dict[str, Any]:
        """Cancel a meeting"""
        
        try:
            # Mock cancellation
            logger.info(f"Cancelled meeting {meeting_id}")
            
            return {
                'success': True,
                'meeting_id': meeting_id,
                'status': 'cancelled'
            }
            
        except Exception as e:
            logger.error(f"Error cancelling meeting: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_google_auth_url(self, user_id: int) -> str:
        """Get Google OAuth authorization URL"""
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
                    }
                },
                scopes=self.google_scopes
            )
            
            flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
            
            authorization_url, state = flow.authorization_url(
                access_type='offline',
                include_granted_scopes='true',
                state=str(user_id)
            )
            
            return authorization_url
            
        except Exception as e:
            logger.error(f"Error generating Google auth URL: {e}")
            return ""
    
    async def handle_google_callback(
        self,
        authorization_code: str,
        user_id: int
    ) -> Dict[str, Any]:
        """Handle Google OAuth callback and store credentials"""
        
        try:
            flow = Flow.from_client_config(
                {
                    "web": {
                        "client_id": settings.GOOGLE_CLIENT_ID,
                        "client_secret": settings.GOOGLE_CLIENT_SECRET,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [settings.GOOGLE_REDIRECT_URI]
                    }
                },
                scopes=self.google_scopes
            )
            
            flow.redirect_uri = settings.GOOGLE_REDIRECT_URI
            flow.fetch_token(code=authorization_code)
            
            credentials = flow.credentials
            
            # TODO: Store credentials securely in database
            # For now, just return success
            
            return {
                'success': True,
                'user_id': user_id,
                'calendar_type': 'google'
            }
            
        except Exception as e:
            logger.error(f"Error handling Google callback: {e}")
            return {'success': False, 'error': str(e)}
