from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import json
from core.database import Base

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    department = Column(String(100))
    location = Column(String(100))
    employment_type = Column(String(50))  # full-time, part-time, contract
    experience_level = Column(String(50))  # entry, mid, senior, executive
    salary_min = Column(Integer)
    salary_max = Column(Integer)
    currency = Column(String(3), default='INR')
    
    # AI Analysis Results
    parsed_skills = Column(Text)  # JSON string of extracted skills
    ai_confidence_score = Column(Float)
    matching_keywords = Column(Text)  # JSON string of keywords
    
    # Status and Workflow
    status = Column(String(20), default='draft')  # draft, active, paused, closed
    priority = Column(String(10), default='medium')  # low, medium, high, urgent
    
    # Metadata
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deadline = Column(DateTime)
    
    # Relationships
    creator = relationship('User', back_populates='created_jobs')
    candidates = relationship('Candidate', back_populates='job', cascade='all, delete-orphan')
    interviews = relationship('Interview', back_populates='job')
    
    @property
    def parsed_skills_list(self):
        if self.parsed_skills:
            try:
                return json.loads(self.parsed_skills)
            except json.JSONDecodeError:
                return []
        return []
    
    @parsed_skills_list.setter
    def parsed_skills_list(self, skills_list):
        self.parsed_skills = json.dumps(skills_list) if skills_list else None
    
    @property
    def matching_keywords_list(self):
        if self.matching_keywords:
            try:
                return json.loads(self.matching_keywords)
            except json.JSONDecodeError:
                return []
        return []
    
    @matching_keywords_list.setter
    def matching_keywords_list(self, keywords_list):
        self.matching_keywords = json.dumps(keywords_list) if keywords_list else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'requirements': self.requirements,
            'department': self.department,
            'location': self.location,
            'employment_type': self.employment_type,
            'experience_level': self.experience_level,
            'salary_min': self.salary_min,
            'salary_max': self.salary_max,
            'currency': self.currency,
            'parsed_skills': self.parsed_skills_list,
            'ai_confidence_score': self.ai_confidence_score,
            'matching_keywords': self.matching_keywords_list,
            'status': self.status,
            'priority': self.priority,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'deadline': self.deadline.isoformat() if self.deadline else None
        }
    
    def __repr__(self):
        return f'<Job {self.title}>'
