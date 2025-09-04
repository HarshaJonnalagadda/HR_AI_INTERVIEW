# models/interview.py

import json
from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, Boolean, Text,
                        ForeignKey)
from sqlalchemy.orm import relationship

# Correctly import the declarative base from your decoupled database file
from core.database import Base

class Interview(Base):
    __tablename__ = 'interviews'
    
    id = Column(Integer, primary_key=True)
    
    # Basic Information
    title = Column(String(200), nullable=False)
    interview_type = Column(String(50), default='technical')  # technical, behavioral, hr, final
    round_number = Column(Integer, default=1)
    
    # Scheduling Information
    scheduled_at = Column(DateTime) # Nullable until confirmed
    duration_minutes = Column(Integer, default=60)
    timezone = Column(String(50))
    
    # Meeting Details
    meeting_link = Column(String(500))  # Google Meet, Teams, Zoom link
    meeting_platform = Column(String(20), default='google_meet')  # google_meet, teams, zoom
    meeting_id = Column(String(100))
    
    # Status Tracking
    status = Column(String(20), default='pending')  
    # pending, scheduled, confirmed, completed, cancelled, rescheduled
    
    # Approval Workflow
    interviewer_approved = Column(Boolean, default=False)
    approved_slots = Column(Text)  # JSON string of approved time slots
    candidate_confirmed = Column(Boolean, default=False)
    
    # Reminders
    reminder_24h_sent = Column(Boolean, default=False)
    reminder_1h_sent = Column(Boolean, default=False)
    
    # Rescheduling
    original_scheduled_at = Column(DateTime)
    reschedule_count = Column(Integer, default=0)
    reschedule_reason = Column(String(500))
    
    # Foreign Key Relationships
    candidate_id = Column(String, ForeignKey('candidates.id'), nullable=False)
    interviewer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # ORM Relationships
    interviewer = relationship('User', back_populates='assigned_interviews')
    job = relationship('Job', back_populates='interviews')
    candidate = relationship('Candidate', back_populates='interviews')
    feedback = relationship('Feedback', backref='interview', lazy=True, cascade='all, delete-orphan')
    
    @property
    def approved_slots_list(self):
        """Gets the JSON string approved_slots and returns it as a list."""
        if self.approved_slots:
            try:
                return json.loads(self.approved_slots)
            except json.JSONDecodeError:
                return []
        return []
    
    @approved_slots_list.setter
    def approved_slots_list(self, slots_list: list):
        """Takes a list and stores it as a JSON string in approved_slots."""
        self.approved_slots = json.dumps(slots_list) if slots_list else None
    
    def to_dict(self):
        """Returns a dictionary representation of the model."""
        return {
            'id': self.id,
            'title': self.title,
            'interview_type': self.interview_type,
            'round_number': self.round_number,
            'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
            'duration_minutes': self.duration_minutes,
            'timezone': self.timezone,
            'meeting_link': self.meeting_link,
            'meeting_platform': self.meeting_platform,
            'meeting_id': self.meeting_id,
            'status': self.status,
            'interviewer_approved': self.interviewer_approved,
            'approved_slots': self.approved_slots_list,
            'candidate_confirmed': self.candidate_confirmed,
            'reminder_24h_sent': self.reminder_24h_sent,
            'reminder_1h_sent': self.reminder_1h_sent,
            'original_scheduled_at': self.original_scheduled_at.isoformat() if self.original_scheduled_at else None,
            'reschedule_count': self.reschedule_count,
            'reschedule_reason': self.reschedule_reason,
            'candidate_id': self.candidate_id,
            'interviewer_id': self.interviewer_id,
            'job_id': self.job_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Interview {self.id} for Candidate {self.candidate_id}>'