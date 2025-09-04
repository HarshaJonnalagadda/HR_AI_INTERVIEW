import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
import httpx
from core.config import settings
from services.ai_service import AIService
from models.candidate import Candidate
from models.job import Job
import logging
import requests
import json

logger = logging.getLogger(__name__)

class OutreachService:
    """Multi-channel outreach service for candidate communication"""
    
    def __init__(self):
        # Initialize Exotel client (primary voice service)
        self.exotel_config = {
            'sid': settings.EXOTEL_SID,
            'api_key': settings.EXOTEL_API_KEY,
            'api_token': settings.EXOTEL_API_TOKEN,
            'phone_number': settings.EXOTEL_PHONE_NUMBER
        } if settings.EXOTEL_SID else None
        
        # Gmail SMTP configuration
        self.gmail_config = {
            'email': settings.GMAIL_EMAIL,
            'password': settings.GMAIL_APP_PASSWORD,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587
        } if settings.GMAIL_EMAIL else None
        
        self.ai_service = AIService()
    
    async def send_initial_outreach(self, candidate: Candidate) -> Dict[str, Any]:
        """Send initial outreach message to candidate"""
        
        try:
            # Get job details
            job = candidate.job  # Assuming relationship is loaded
            
            # Generate personalized message using AI
            message_data = await self.ai_service.generate_outreach_message(
                candidate_profile=candidate.to_dict(),
                job_details=job.to_dict(),
                message_type="initial_contact"
            )
            
            # Send via preferred channel
            if candidate.preferred_contact_method == "email":
                result = await self._send_email(
                    to_email=candidate.email,
                    subject=message_data.get('subject', ''),
                    content=message_data.get('message', ''),
                    candidate_name=candidate.full_name
                )
            elif candidate.preferred_contact_method == "sms" and candidate.phone:
                result = await self._send_sms(
                    to_phone=candidate.phone,
                    message=message_data.get('sms_version', message_data.get('message', '')[:140]),
                    candidate_name=candidate.full_name
                )
            else:
                # Default to email
                result = await self._send_email(
                    to_email=candidate.email,
                    subject=message_data.get('subject', ''),
                    content=message_data.get('message', ''),
                    candidate_name=candidate.full_name
                )
            
            return {
                'success': result.get('success', False),
                'channel': candidate.preferred_contact_method,
                'message_id': result.get('message_id'),
                'personalization_elements': message_data.get('personalization_elements', [])
            }
            
        except Exception as e:
            logger.error(f"Outreach error for candidate {candidate.id}: {e}")
            return {
                'success': False,
                'error': str(e),
                'channel': candidate.preferred_contact_method
            }
    
    async def _send_email(
        self, 
        to_email: str, 
        subject: str, 
        content: str, 
        candidate_name: str
    ) -> Dict[str, Any]:
        """Send email using Gmail SMTP"""
        
        if not self.gmail_config:
            logger.error("Gmail SMTP not configured")
            return {'success': False, 'error': 'Email service not configured'}
        
        try:
            # Add India compliance footer
            compliance_footer = """
            
            ---
            This message was sent by an automated recruitment system. 
            Reply 'STOP' to opt-out of future communications.
            Your data is processed in accordance with applicable privacy laws.
            """
            
            full_content = content + compliance_footer
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{settings.FROM_NAME} <{self.gmail_config['email']}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Reply-To'] = settings.REPLY_TO_EMAIL or self.gmail_config['email']
            
            # Add body
            msg.attach(MIMEText(full_content, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.gmail_config['smtp_server'], self.gmail_config['smtp_port'])
            server.starttls()
            server.login(self.gmail_config['email'], self.gmail_config['password'])
            text = msg.as_string()
            server.sendmail(self.gmail_config['email'], to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            
            return {
                'success': True,
                'message_id': f"gmail_{hash(to_email + subject)}",
                'status_code': 200
            }
            
        except Exception as e:
            logger.error(f"Email sending error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def _send_sms(
        self, 
        to_phone: str, 
        message: str, 
        candidate_name: str
    ) -> Dict[str, Any]:
        """Send SMS using Exotel"""
        
        if not self.exotel_config:
            logger.error("Exotel client not configured")
            return {'success': False, 'error': 'SMS service not configured'}
        
        try:
            # Add compliance message
            compliance_message = f"{message} Reply STOP to opt-out."
            
            # Ensure message is under 160 characters
            if len(compliance_message) > 160:
                compliance_message = message[:140] + "... Reply STOP to opt-out."
            
            # Exotel SMS API endpoint
            url = f"https://api.exotel.com/v1/Accounts/{self.exotel_config['sid']}/Sms/send.json"
            
            payload = {
                'From': self.exotel_config['phone_number'],
                'To': to_phone,
                'Body': compliance_message
            }
            
            response = requests.post(
                url,
                auth=(self.exotel_config['api_key'], self.exotel_config['api_token']),
                data=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    'success': True,
                    'message_id': result.get('SMSMessage', {}).get('Sid'),
                    'status': result.get('SMSMessage', {}).get('Status')
                }
            else:
                logger.error(f"Exotel SMS error: {response.text}")
                return {'success': False, 'error': f'SMS API error: {response.status_code}'}
            
        except Exception as e:
            logger.error(f"SMS sending error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def send_interview_invitation(
        self, 
        candidate: Candidate, 
        interview_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send interview invitation to candidate"""
        
        try:
            subject = f"Interview Invitation - {interview_details.get('job_title', '')}"
            
            content = f"""
            Dear {candidate.first_name},
            
            We are pleased to invite you for an interview for the position of {interview_details.get('job_title', '')}.
            
            Interview Details:
            - Date & Time: {interview_details.get('scheduled_at', '')}
            - Duration: {interview_details.get('duration_minutes', 60)} minutes
            - Meeting Link: {interview_details.get('meeting_link', '')}
            - Interviewer: {interview_details.get('interviewer_name', '')}
            
            Please confirm your attendance by replying to this email.
            
            Tech Check: {interview_details.get('tech_check_link', 'Test your setup before the interview')}
            
            Best regards,
            HR Team
            """
            
            return await self._send_email(
                to_email=candidate.email,
                subject=subject,
                content=content,
                candidate_name=candidate.full_name
            )
            
        except Exception as e:
            logger.error(f"Interview invitation error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def send_interview_reminder(
        self, 
        candidate: Candidate, 
        interview_details: Dict[str, Any],
        reminder_type: str = "24h"
    ) -> Dict[str, Any]:
        """Send interview reminder"""
        
        try:
            if reminder_type == "24h":
                subject = "Interview Reminder - Tomorrow"
                time_text = "tomorrow"
            else:
                subject = "Interview Reminder - Starting Soon"
                time_text = "in 1 hour"
            
            content = f"""
            Dear {candidate.first_name},
            
            This is a reminder that you have an interview scheduled {time_text}.
            
            Interview Details:
            - Position: {interview_details.get('job_title', '')}
            - Time: {interview_details.get('scheduled_at', '')}
            - Meeting Link: {interview_details.get('meeting_link', '')}
            
            Please ensure you have a stable internet connection and test your audio/video beforehand.
            
            Best regards,
            HR Team
            """
            
            # Send both email and SMS for 1-hour reminder
            email_result = await self._send_email(
                to_email=candidate.email,
                subject=subject,
                content=content,
                candidate_name=candidate.full_name
            )
            
            sms_result = None
            if reminder_type == "1h" and candidate.phone:
                sms_message = f"Interview reminder: {interview_details.get('job_title', '')} starts in 1 hour. Link: {interview_details.get('meeting_link', '')}"
                sms_result = await self._send_sms(
                    to_phone=candidate.phone,
                    message=sms_message,
                    candidate_name=candidate.full_name
                )
            
            return {
                'email_result': email_result,
                'sms_result': sms_result,
                'reminder_type': reminder_type
            }
            
        except Exception as e:
            logger.error(f"Interview reminder error: {e}")
            return {'success': False, 'error': str(e)}
    
    async def send_feedback_email(
        self, 
        candidate: Candidate, 
        feedback_content: str,
        is_positive: bool = True
    ) -> Dict[str, Any]:
        """Send interview feedback to candidate"""
        
        try:
            if is_positive:
                subject = "Thank you for your interview - Next Steps"
            else:
                subject = "Thank you for your interview"
            
            return await self._send_email(
                to_email=candidate.email,
                subject=subject,
                content=feedback_content,
                candidate_name=candidate.full_name
            )
            
        except Exception as e:
            logger.error(f"Feedback email error: {e}")
            return {'success': False, 'error': str(e)}
