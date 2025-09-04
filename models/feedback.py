from core.database import Base
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime, String, Boolean
from datetime import datetime
import json

class Feedback(Base):
    __tablename__ = 'feedback'
    
    id = Column(Integer, primary_key=True)
    
    # Interview Outcome
    overall_rating = Column(Integer)  # 1-5 scale
    recommendation = Column(String(20))  # hire, no_hire, maybe, strong_hire
    
    # Detailed Feedback
    technical_skills_rating = Column(Integer)  # 1-5 scale
    communication_rating = Column(Integer)  # 1-5 scale
    cultural_fit_rating = Column(Integer)  # 1-5 scale
    problem_solving_rating = Column(Integer)  # 1-5 scale
    
    # Comments
    strengths = Column(Text)
    weaknesses = Column(Text)
    detailed_comments = Column(Text)
    questions_asked =   Column(Text)  # JSON string of questions
    
    # AI Generated Content
    ai_draft_feedback = Column(Text)
    ai_draft_approved = Column(Boolean, default=False)
    hr_customized_feedback = Column(Text)
    
    # Status
    status = Column(String(20), default='draft')  # draft, pending_approval, approved, sent
    feedback_sent_at = Column(DateTime)
    
    # Relationships
    interview_id = Column(Integer, ForeignKey('interviews.id'), nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def questions_asked_list(self):
        if self.questions_asked:
            try:
                return json.loads(self.questions_asked)
            except json.JSONDecodeError:
                return []
        return []
    
    @questions_asked_list.setter
    def questions_asked_list(self, questions_list):
        self.questions_asked = json.dumps(questions_list) if questions_list else None
    
    def to_dict(self):
        return {
            'id': self.id,
            'overall_rating': self.overall_rating,
            'recommendation': self.recommendation,
            'technical_skills_rating': self.technical_skills_rating,
            'communication_rating': self.communication_rating,
            'cultural_fit_rating': self.cultural_fit_rating,
            'problem_solving_rating': self.problem_solving_rating,
            'strengths': self.strengths,
            'weaknesses': self.weaknesses,
            'detailed_comments': self.detailed_comments,
            'questions_asked': self.questions_asked_list,
            'ai_draft_feedback': self.ai_draft_feedback,
            'ai_draft_approved': self.ai_draft_approved,
            'hr_customized_feedback': self.hr_customized_feedback,
            'status': self.status,
            'feedback_sent_at': self.feedback_sent_at.isoformat() if self.feedback_sent_at else None,
            'interview_id': self.interview_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Feedback {self.id} - {self.recommendation}>'
