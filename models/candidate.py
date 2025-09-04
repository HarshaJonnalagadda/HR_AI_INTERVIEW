from core.database import Base
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import json
import uuid

class Candidate(Base):
    __tablename__ = 'candidates'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Basic Information
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), nullable=False, index=True)
    phone = Column(String(20))
    linkedin_url = Column(String(255))
    resume_url = Column(String(255))
    
    # Professional Information
    current_title = Column(String(200))
    current_company = Column(String(200))
    experience_years = Column(Integer)
    skills = Column(Text)  # JSON string of skills
    location = Column(String(100))
    
    # AI Analysis
    ai_confidence_score = Column(Float)
    matching_rationale = Column(Text)
    parsed_resume_data = Column(Text)  # JSON string of extracted data
    
    # Recruitment Status
    status = Column(String(20), default='sourced')
    source = Column(String(50))  # linkedin, indeed, referral, etc.
    
    # Communication Preferences
    preferred_contact_method = Column(String(20), default='email')  # email, phone, sms
    timezone = Column(String(50))
    
    # Compensation Expectations
    expected_salary_min = Column(Integer)
    expected_salary_max = Column(Integer)
    notice_period_days = Column(Integer)
    
    # Relationships
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_contacted_at = Column(DateTime)
    
    # Relationships
    job = relationship("Job", back_populates="candidates")
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def skills_list(self):
        if self.skills:
            try:
                return json.loads(self.skills)
            except json.JSONDecodeError:
                return []
        return []
    
    @skills_list.setter
    def skills_list(self, skills_list):
        self.skills = json.dumps(skills_list) if skills_list else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'linkedin_url': self.linkedin_url,
            'current_title': self.current_title,
            'current_company': self.current_company,
            'experience_years': self.experience_years,
            'skills': self.skills_list,
            'location': self.location,
            'ai_confidence_score': self.ai_confidence_score,
            'status': self.status,
            'source': self.source,
            'job_id': self.job_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Candidate {self.full_name}>'
