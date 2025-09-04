# models/negotiation.py

from core.database import Base
from sqlalchemy import (Column, Integer, Text, ForeignKey, DateTime, 
                        String, Boolean, Date, func)
from datetime import datetime
import json

class Negotiation(Base):
    __tablename__ = 'negotiations'
    
    id = Column(Integer, primary_key=True)
    
    # Candidate Expectations (Pre-Call Data Collection)
    expected_salary = Column(Integer)
    expected_currency = Column(String(3), default='USD')
    notice_period_days = Column(Integer)
    preferred_start_date = Column(Date)
    work_arrangement_preference = Column(String(20))  # remote, hybrid, onsite
    other_preferences = Column(Text)  # JSON string of additional preferences
    
    # Company Offer Details
    offered_salary = Column(Integer)
    offered_currency = Column(String(3), default='USD')
    offered_benefits = Column(Text)  # JSON string of benefits
    offered_start_date = Column(Date)
    offered_work_arrangement = Column(String(20))
    
    # AI Strategy and Analysis
    market_salary_data = Column(Text)  # JSON string of market analysis
    negotiation_strategy = Column(Text)  # AI-generated strategy
    recommended_offer = Column(Integer)
    counter_offer_scenarios = Column(Text)  # JSON string of scenarios
    key_talking_points = Column(Text)  # JSON string of talking points
    
    # Negotiation Process
    status = Column(String(20), default='data_collection')  
    # data_collection, strategy_prepared, call_scheduled, in_negotiation, 
    # verbal_agreement, offer_sent, accepted, rejected, withdrawn
    
    negotiation_call_scheduled_at = Column(DateTime)
    negotiation_call_completed_at = Column(DateTime)
    negotiation_notes = Column(Text)
    
    # Final Agreement
    final_salary = Column(Integer)
    final_benefits = Column(Text)  # JSON string
    final_start_date = Column(Date)
    final_work_arrangement = Column(String(20))
    
    # Offer Letter
    offer_letter_generated = Column(Boolean, default=False)
    offer_letter_url = Column(String(500))
    offer_sent_at = Column(DateTime)
    offer_accepted_at = Column(DateTime)
    offer_rejected_at = Column(DateTime)
    rejection_reason = Column(Text)
    
    # Relationships
    candidate_id = Column(String, ForeignKey('candidates.id'), nullable=False)
    
    # Metadata (Corrected timestamp handling)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    @property
    def other_preferences_dict(self):
        if self.other_preferences:
            try:
                return json.loads(self.other_preferences)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @other_preferences_dict.setter
    def other_preferences_dict(self, prefs_dict):
        self.other_preferences = json.dumps(prefs_dict) if prefs_dict else None
    
    @property
    def offered_benefits_list(self):
        if self.offered_benefits:
            try:
                return json.loads(self.offered_benefits)
            except json.JSONDecodeError:
                return []
        return []
    
    @offered_benefits_list.setter
    def offered_benefits_list(self, benefits_list):
        self.offered_benefits = json.dumps(benefits_list) if benefits_list else None
    
    @property
    def market_salary_dict(self):
        if self.market_salary_data:
            try:
                return json.loads(self.market_salary_data)
            except json.JSONDecodeError:
                return {}
        return {}
    
    @market_salary_dict.setter
    def market_salary_dict(self, data_dict):
        self.market_salary_data = json.dumps(data_dict) if data_dict else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'expected_salary': self.expected_salary,
            'expected_currency': self.expected_currency,
            'notice_period_days': self.notice_period_days,
            'preferred_start_date': self.preferred_start_date.isoformat() if self.preferred_start_date else None,
            'work_arrangement_preference': self.work_arrangement_preference,
            'other_preferences': self.other_preferences_dict,
            'offered_salary': self.offered_salary,
            'offered_currency': self.offered_currency,
            'offered_benefits': self.offered_benefits_list,
            'offered_start_date': self.offered_start_date.isoformat() if self.offered_start_date else None,
            'offered_work_arrangement': self.offered_work_arrangement,
            'market_salary_data': self.market_salary_dict,
            'negotiation_strategy': self.negotiation_strategy,
            'recommended_offer': self.recommended_offer,
            'status': self.status,
            'negotiation_call_scheduled_at': self.negotiation_call_scheduled_at.isoformat() if self.negotiation_call_scheduled_at else None,
            'negotiation_call_completed_at': self.negotiation_call_completed_at.isoformat() if self.negotiation_call_completed_at else None,
            'negotiation_notes': self.negotiation_notes,
            'final_salary': self.final_salary,
            'final_start_date': self.final_start_date.isoformat() if self.final_start_date else None,
            'final_work_arrangement': self.final_work_arrangement,
            'offer_letter_generated': self.offer_letter_generated,
            'offer_letter_url': self.offer_letter_url,
            'offer_sent_at': self.offer_sent_at.isoformat() if self.offer_sent_at else None,
            'offer_accepted_at': self.offer_accepted_at.isoformat() if self.offer_accepted_at else None,
            'offer_rejected_at': self.offer_rejected_at.isoformat() if self.offer_rejected_at else None,
            'rejection_reason': self.rejection_reason,
            'candidate_id': self.candidate_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Negotiation {self.id} for Candidate {self.candidate_id} - Status: {self.status}>'