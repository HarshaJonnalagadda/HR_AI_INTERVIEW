"""
Multi-provider email service supporting Gmail, Outlook, and custom SMTP
Cost-effective alternative to SendGrid for Indian operations
"""

import asyncio
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Dict, Any
from enum import Enum
import structlog
from pathlib import Path

from core.config import settings

logger = structlog.get_logger()

class EmailProvider(str, Enum):
    GMAIL = "gmail"
    OUTLOOK = "outlook"
    CUSTOM_SMTP = "custom_smtp"
    SENDGRID = "sendgrid"

class EmailService:
    """Multi-provider email service with fallback support"""
    
    def __init__(self):
        self.primary_provider = self._get_primary_provider()
        self.fallback_providers = self._get_fallback_providers()
    
    def _get_primary_provider(self) -> EmailProvider:
        """Determine primary email provider based on configuration"""
        if settings.GMAIL_EMAIL and settings.GMAIL_APP_PASSWORD:
            return EmailProvider.GMAIL
        elif settings.OUTLOOK_EMAIL and settings.OUTLOOK_PASSWORD:
            return EmailProvider.OUTLOOK
        elif settings.SMTP_HOST and settings.SMTP_USERNAME:
            return EmailProvider.CUSTOM_SMTP
        elif settings.SENDGRID_API_KEY:
            return EmailProvider.SENDGRID
        else:
            raise ValueError("No email provider configured")
    
    def _get_fallback_providers(self) -> List[EmailProvider]:
        """Get list of fallback providers"""
        providers = []
        if settings.SENDGRID_API_KEY:
            providers.append(EmailProvider.SENDGRID)
        if settings.GMAIL_EMAIL and settings.GMAIL_APP_PASSWORD:
            providers.append(EmailProvider.GMAIL)
        if settings.OUTLOOK_EMAIL and settings.OUTLOOK_PASSWORD:
            providers.append(EmailProvider.OUTLOOK)
        return [p for p in providers if p != self.primary_provider]
    
    async def send_email(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[str]] = None,
        provider: Optional[EmailProvider] = None
    ) -> Dict[str, Any]:
        """
        Send email using specified or primary provider
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            html_content: HTML email content
            text_content: Plain text content (optional)
            attachments: List of file paths to attach
            provider: Specific provider to use
            
        Returns:
            Dict with send status and details
        """
        provider = provider or self.primary_provider
        
        try:
            if provider == EmailProvider.GMAIL:
                result = await self._send_gmail(to_emails, subject, html_content, text_content, attachments)
            elif provider == EmailProvider.OUTLOOK:
                result = await self._send_outlook(to_emails, subject, html_content, text_content, attachments)
            elif provider == EmailProvider.CUSTOM_SMTP:
                result = await self._send_custom_smtp(to_emails, subject, html_content, text_content, attachments)
            else:
                result = await self._send_sendgrid(to_emails, subject, html_content, text_content, attachments)
            
            logger.info(
                "Email sent successfully",
                provider=provider,
                to_count=len(to_emails),
                subject=subject[:50]
            )
            
            return result
            
        except Exception as e:
            logger.error(
                "Email send failed",
                provider=provider,
                error=str(e),
                to_count=len(to_emails)
            )
            
            # Try fallback provider
            if provider == self.primary_provider and self.fallback_providers:
                logger.info("Trying fallback email provider", fallback=self.fallback_providers[0])
                return await self.send_email(
                    to_emails, subject, html_content, text_content, 
                    attachments, self.fallback_providers[0]
                )
            
            return {
                "success": False,
                "error": str(e),
                "provider": provider
            }
    
    async def _send_gmail(
        self, 
        to_emails: List[str], 
        subject: str, 
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send email using Gmail SMTP"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{settings.FROM_NAME} <{settings.GMAIL_EMAIL}>"
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        msg['Reply-To'] = settings.REPLY_TO_EMAIL or settings.GMAIL_EMAIL
        
        # Add text and HTML parts
        if text_content:
            msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Add attachments
        if attachments:
            for file_path in attachments:
                self._add_attachment(msg, file_path)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls(context=context)
            server.login(settings.GMAIL_EMAIL, settings.GMAIL_APP_PASSWORD)
            server.send_message(msg)
        
        return {
            "success": True,
            "provider": EmailProvider.GMAIL,
            "message_id": "gmail_sent",
            "cost": "Free (up to 500/day)"
        }
    
    async def _send_outlook(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send email using Outlook SMTP"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{settings.FROM_NAME} <{settings.OUTLOOK_EMAIL}>"
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        msg['Reply-To'] = settings.REPLY_TO_EMAIL or settings.OUTLOOK_EMAIL
        
        # Add text and HTML parts
        if text_content:
            msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Add attachments
        if attachments:
            for file_path in attachments:
                self._add_attachment(msg, file_path)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
            server.starttls(context=context)
            server.login(settings.OUTLOOK_EMAIL, settings.OUTLOOK_PASSWORD)
            server.send_message(msg)
        
        return {
            "success": True,
            "provider": EmailProvider.OUTLOOK,
            "message_id": "outlook_sent",
            "cost": "Free (up to 300/day)"
        }
    
    async def _send_custom_smtp(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send email using custom SMTP server"""
        
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{settings.FROM_NAME} <{settings.SMTP_USERNAME}>"
        msg['To'] = ', '.join(to_emails)
        msg['Subject'] = subject
        msg['Reply-To'] = settings.REPLY_TO_EMAIL or settings.SMTP_USERNAME
        
        # Add text and HTML parts
        if text_content:
            msg.attach(MIMEText(text_content, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))
        
        # Add attachments
        if attachments:
            for file_path in attachments:
                self._add_attachment(msg, file_path)
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls(context=context)
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        return {
            "success": True,
            "provider": EmailProvider.CUSTOM_SMTP,
            "message_id": "custom_smtp_sent",
            "cost": "Domain hosting cost"
        }
    
    async def _send_sendgrid(
        self,
        to_emails: List[str],
        subject: str,
        html_content: str,
        text_content: str,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send email using SendGrid API (fallback) - DISABLED"""
        logger.warning("SendGrid provider disabled - use Gmail SMTP instead")
        return {
            "success": False,
            "error": "SendGrid provider disabled",
            "provider": "sendgrid"
        }
    
    def _add_attachment(self, msg: MIMEMultipart, file_path: str):
        """Add file attachment to email message"""
        try:
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {Path(file_path).name}'
            )
            msg.attach(part)
        except Exception as e:
            logger.error("Failed to add attachment", file_path=file_path, error=str(e))

# Email templates for common use cases
class EmailTemplates:
    """Pre-built email templates for recruitment workflows"""
    
    @staticmethod
    def interview_invitation(candidate_name: str, job_title: str, interview_time: str, meeting_link: str) -> Dict[str, str]:
        """Interview invitation email template"""
        subject = f"Interview Invitation - {job_title} Position"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c5aa0;">Interview Invitation</h2>
                
                <p>Dear {candidate_name},</p>
                
                <p>We are pleased to invite you for an interview for the <strong>{job_title}</strong> position at {settings.COMPANY_NAME}.</p>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Interview Details:</h3>
                    <p><strong>Date & Time:</strong> {interview_time}</p>
                    <p><strong>Meeting Link:</strong> <a href="{meeting_link}">{meeting_link}</a></p>
                </div>
                
                <p>Please confirm your availability by replying to this email.</p>
                
                <p>Best regards,<br>
                {settings.FROM_NAME}</p>
            </div>
        </body>
        </html>
        """
        
        text_content = f"""
        Interview Invitation - {job_title} Position
        
        Dear {candidate_name},
        
        We are pleased to invite you for an interview for the {job_title} position at {settings.COMPANY_NAME}.
        
        Interview Details:
        Date & Time: {interview_time}
        Meeting Link: {meeting_link}
        
        Please confirm your availability by replying to this email.
        
        Best regards,
        {settings.FROM_NAME}
        """
        
        return {
            "subject": subject,
            "html_content": html_content,
            "text_content": text_content
        }
    
    @staticmethod
    def job_offer(candidate_name: str, job_title: str, salary: str, start_date: str) -> Dict[str, str]:
        """Job offer email template"""
        subject = f"Job Offer - {job_title} Position"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #28a745;">Congratulations! Job Offer</h2>
                
                <p>Dear {candidate_name},</p>
                
                <p>We are delighted to offer you the position of <strong>{job_title}</strong> at {settings.COMPANY_NAME}.</p>
                
                <div style="background-color: #d4edda; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h3 style="margin-top: 0;">Offer Details:</h3>
                    <p><strong>Position:</strong> {job_title}</p>
                    <p><strong>Salary:</strong> {salary}</p>
                    <p><strong>Start Date:</strong> {start_date}</p>
                </div>
                
                <p>Please review the attached offer letter and let us know your decision by replying to this email.</p>
                
                <p>We look forward to welcoming you to our team!</p>
                
                <p>Best regards,<br>
                {settings.FROM_NAME}</p>
            </div>
        </body>
        </html>
        """
        
        return {
            "subject": subject,
            "html_content": html_content,
            "text_content": f"Job Offer - {job_title}\n\nDear {candidate_name},\n\nWe are delighted to offer you the position of {job_title} at {settings.COMPANY_NAME}.\n\nSalary: {salary}\nStart Date: {start_date}\n\nPlease review the attached offer letter.\n\nBest regards,\n{settings.FROM_NAME}"
        }

# Convenience functions
async def send_interview_invitation(
    candidate_email: str,
    candidate_name: str,
    job_title: str,
    interview_time: str,
    meeting_link: str
) -> Dict[str, Any]:
    """Send interview invitation email"""
    service = EmailService()
    template = EmailTemplates.interview_invitation(candidate_name, job_title, interview_time, meeting_link)
    
    return await service.send_email(
        to_emails=[candidate_email],
        subject=template["subject"],
        html_content=template["html_content"],
        text_content=template["text_content"]
    )

async def send_job_offer(
    candidate_email: str,
    candidate_name: str,
    job_title: str,
    salary: str,
    start_date: str,
    offer_letter_path: Optional[str] = None
) -> Dict[str, Any]:
    """Send job offer email"""
    service = EmailService()
    template = EmailTemplates.job_offer(candidate_name, job_title, salary, start_date)
    
    attachments = [offer_letter_path] if offer_letter_path else None
    
    return await service.send_email(
        to_emails=[candidate_email],
        subject=template["subject"],
        html_content=template["html_content"],
        text_content=template["text_content"],
        attachments=attachments
    )
