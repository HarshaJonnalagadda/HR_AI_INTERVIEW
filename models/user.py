from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base
from core.security import get_password_hash, verify_password

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    role = Column(String(20), nullable=False, default='hr_manager')  # hr_manager, interviewer, admin
    department = Column(String(50))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Calendar integration
    google_calendar_id = Column(String(255))
    microsoft_calendar_id = Column(String(255))
    calendar_sync_enabled = Column(Boolean, default=False)
    
    # Relationships
    created_jobs = relationship('Job', back_populates='creator', foreign_keys='Job.created_by')
    assigned_interviews = relationship('Interview', back_populates='interviewer', foreign_keys='Interview.interviewer_id')
    
    def set_password(self, password: str):
        self.password_hash = get_password_hash(password)
    
    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password_hash)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'role': self.role,
            'department': self.department,
            'phone': self.phone,
            'is_active': self.is_active,
            'calendar_sync_enabled': self.calendar_sync_enabled,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
