from core.database import Base
from sqlalchemy import (Column, Integer, String, Text, ForeignKey, DateTime, 
                        Boolean, Date, func)
from datetime import datetime
import json

class Outreach(Base):
    __tablename__ = 'outreach'
    
    id = Column(Integer, primary_key=True)
    
    # Outreach Details
    channel = Column(String(20), nullable=False)  # email, sms, phone, ai_call
    message_type = Column(String(30), nullable=False)  # initial_contact, follow_up, reminder, interview_invite
    
    # Content
    subject = Column(String(200))  # For emails
    message_content = Column(Text, nullable=False)
    personalized_content = Column(Text)  # AI-personalized version
    
    # AI Call Specific
    call_duration_seconds = Column(Integer)
    call_transcript =  Column(Text)
    call_outcome = Column(String(50))  # completed, no_answer, declined, interested
    
    # Status and Tracking
    status = Column(String(20), default='pending')  # pending, sent, delivered, opened, replied, failed
    sent_at = Column(DateTime)
    delivered_at = Column(DateTime)
    opened_at = Column(DateTime)
    replied_at = Column(DateTime)
    
    # Response Tracking
    candidate_response = Column(Text)
    response_sentiment = Column(String(20))  # positive, negative, neutral, interested, not_interested
    
    # External IDs
    external_message_id = Column(String(100))  # Twilio SID, SendGrid ID, etc.
    
    # Relationships
    candidate_id = Column(String, ForeignKey('candidates.id'), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, server_default=func.now())  
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'channel': self.channel,
            'message_type': self.message_type,
            'subject': self.subject,
            'message_content': self.message_content,
            'personalized_content': self.personalized_content,
            'call_duration_seconds': self.call_duration_seconds,
            'call_transcript': self.call_transcript,
            'call_outcome': self.call_outcome,
            'status': self.status,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None,
            'opened_at': self.opened_at.isoformat() if self.opened_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None,
            'candidate_response': self.candidate_response,
            'response_sentiment': self.response_sentiment,
            'external_message_id': self.external_message_id,
            'candidate_id': self.candidate_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Outreach {self.channel} - {self.message_type}>'
