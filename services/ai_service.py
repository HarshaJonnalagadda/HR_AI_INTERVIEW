import asyncio
from typing import List, Dict, Optional, Any
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage
from langchain.memory import ConversationBufferMemory
import openai
from core.config import settings
import logging
import json
import re

logger = logging.getLogger(__name__)

class AIService:
    """Agentic AI service using OpenAI and LangChain for recruitment automation"""
    
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    
    async def analyze_job_description(self, job_description: str, requirements: str = "") -> Dict[str, Any]:
        """AI agent to analyze job description and extract key information"""
        
        prompt = f"""
        Analyze this job description and requirements to extract structured information for candidate sourcing.
        
        Job Description:
        {job_description}
        
        Requirements:
        {requirements}
        
        Extract and return a JSON object with:
        1. skills: List of technical and soft skills (max 15)
        2. experience_level: entry/mid/senior/executive
        3. keywords: List of search keywords for LinkedIn (max 10)
        4. confidence_score: Float 0-1 indicating analysis confidence
        5. salary_estimate: Estimated salary range in INR
        6. location_preferences: Likely work locations
        7. must_have_skills: Critical skills (max 5)
        8. nice_to_have_skills: Preferred skills (max 5)
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Job analysis completed with confidence: {result.get('confidence_score', 0)}")
            
            return result
            
        except Exception as e:
            logger.error(f"Job analysis error: {e}")
            return {
                "skills": [],
                "experience_level": "mid",
                "keywords": [],
                "confidence_score": 0.0,
                "salary_estimate": {"min": 0, "max": 0},
                "location_preferences": ["India"],
                "must_have_skills": [],
                "nice_to_have_skills": []
            }
    
    async def analyze_candidate_match(self, candidate_profile: Dict, job_requirements: Dict) -> Dict[str, Any]:
        """AI agent to analyze candidate-job match"""
        
        prompt = f"""
        Analyze how well this candidate matches the job requirements.
        
        Candidate Profile:
        - Name: {candidate_profile.get('first_name', '')} {candidate_profile.get('last_name', '')}
        - Current Title: {candidate_profile.get('current_title', '')}
        - Current Company: {candidate_profile.get('current_company', '')}
        - Experience: {candidate_profile.get('experience_years', 0)} years
        - Skills: {candidate_profile.get('skills', [])}
        - Location: {candidate_profile.get('location', '')}
        - Summary: {candidate_profile.get('summary', '')}
        
        Job Requirements:
        - Title: {job_requirements.get('title', '')}
        - Required Skills: {job_requirements.get('parsed_skills_list', [])}
        - Experience Level: {job_requirements.get('experience_level', '')}
        - Location: {job_requirements.get('location', '')}
        
        Return JSON with:
        1. confidence_score: Float 0-1 (overall match score)
        2. rationale: String explaining the match reasoning
        3. skill_match_score: Float 0-1 (skills alignment)
        4. experience_match_score: Float 0-1 (experience fit)
        5. location_match_score: Float 0-1 (location compatibility)
        6. strengths: List of candidate strengths for this role
        7. concerns: List of potential concerns or gaps
        8. recommendation: hire/maybe/no_hire
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Candidate match analysis: {result.get('confidence_score', 0)} confidence")
            
            return result
            
        except Exception as e:
            logger.error(f"Candidate match analysis error: {e}")
            return {
                "confidence_score": 0.5,
                "rationale": "Unable to analyze match",
                "skill_match_score": 0.5,
                "experience_match_score": 0.5,
                "location_match_score": 0.5,
                "strengths": [],
                "concerns": ["Analysis unavailable"],
                "recommendation": "maybe"
            }
    
    async def generate_outreach_message(
        self, 
        candidate_profile: Dict, 
        job_details: Dict, 
        message_type: str = "initial_contact"
    ) -> Dict[str, str]:
        """AI agent to generate personalized outreach messages"""
        
        prompt = f"""
        Generate a personalized {message_type} message for this candidate.
        
        Candidate: {candidate_profile.get('first_name', '')} {candidate_profile.get('last_name', '')}
        Current Role: {candidate_profile.get('current_title', '')} at {candidate_profile.get('current_company', '')}
        
        Job Opportunity:
        - Title: {job_details.get('title', '')}
        - Company: [Company Name]
        - Location: {job_details.get('location', '')}
        - Key Requirements: {job_details.get('parsed_skills_list', [])[:3]}
        
        Message Guidelines:
        - Professional and respectful tone
        - Personalized based on candidate's background
        - Clear value proposition
        - Include consent request for India compliance
        - Keep under 150 words
        - Include clear next steps
        
        Return JSON with:
        1. subject: Email subject line
        2. message: Full message content
        3. sms_version: Shorter SMS version (under 160 chars)
        4. personalization_elements: List of personalized touches used
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info(f"Generated {message_type} message for candidate")
            
            return result
            
        except Exception as e:
            logger.error(f"Message generation error: {e}")
            return {
                "subject": f"Opportunity: {job_details.get('title', 'New Role')}",
                "message": f"Hi {candidate_profile.get('first_name', '')}, I found your profile interesting for a {job_details.get('title', '')} role. Would you be open to learning more? Reply 'INTERESTED' or 'STOP' to opt-out.",
                "sms_version": f"Hi {candidate_profile.get('first_name', '')}, interested in {job_details.get('title', '')} role? Reply INTERESTED or STOP",
                "personalization_elements": []
            }
    
    async def generate_interview_feedback_draft(
        self, 
        interview_data: Dict, 
        feedback_ratings: Dict
    ) -> Dict[str, str]:
        """AI agent to draft interview feedback"""
        
        prompt = f"""
        Generate professional interview feedback based on the ratings and notes.
        
        Interview Details:
        - Candidate: {interview_data.get('candidate_name', '')}
        - Position: {interview_data.get('job_title', '')}
        - Interview Type: {interview_data.get('interview_type', '')}
        - Duration: {interview_data.get('duration_minutes', 60)} minutes
        
        Ratings (1-5 scale):
        - Technical Skills: {feedback_ratings.get('technical_skills_rating', 0)}
        - Communication: {feedback_ratings.get('communication_rating', 0)}
        - Cultural Fit: {feedback_ratings.get('cultural_fit_rating', 0)}
        - Problem Solving: {feedback_ratings.get('problem_solving_rating', 0)}
        - Overall: {feedback_ratings.get('overall_rating', 0)}
        
        Interviewer Notes:
        - Strengths: {feedback_ratings.get('strengths', '')}
        - Weaknesses: {feedback_ratings.get('weaknesses', '')}
        - Comments: {feedback_ratings.get('detailed_comments', '')}
        
        Generate professional feedback email draft that:
        1. Thanks candidate for their time
        2. Provides constructive feedback
        3. Mentions next steps (if positive) or encouragement (if negative)
        4. Maintains professional tone
        5. Is appropriate for India market
        
        Return JSON with:
        1. email_subject: Professional subject line
        2. email_body: Complete feedback email
        3. internal_summary: Brief summary for HR team
        4. recommendation: Clear hire/no-hire recommendation with reasoning
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("Generated interview feedback draft")
            
            return result
            
        except Exception as e:
            logger.error(f"Feedback generation error: {e}")
            return {
                "email_subject": "Thank you for your interview",
                "email_body": "Thank you for taking the time to interview with us. We will be in touch soon with next steps.",
                "internal_summary": "Feedback generation failed",
                "recommendation": "Review required"
            }
    
    async def generate_negotiation_strategy(
        self, 
        candidate_expectations: Dict, 
        company_budget: Dict, 
        market_data: Dict
    ) -> Dict[str, Any]:
        """AI agent to generate negotiation strategy"""
        
        prompt = f"""
        Generate a negotiation strategy for this offer discussion.
        
        Candidate Expectations:
        - Expected Salary: ₹{candidate_expectations.get('expected_salary', 0):,}
        - Notice Period: {candidate_expectations.get('notice_period_days', 0)} days
        - Work Arrangement: {candidate_expectations.get('work_arrangement_preference', '')}
        - Other Preferences: {candidate_expectations.get('other_preferences', {})}
        
        Company Budget:
        - Budget Range: ₹{company_budget.get('min', 0):,} - ₹{company_budget.get('max', 0):,}
        - Benefits Available: {company_budget.get('benefits', [])}
        - Flexibility: {company_budget.get('flexibility_notes', '')}
        
        Market Data:
        - Market Average: ₹{market_data.get('average_salary', 0):,}
        - Market Range: ₹{market_data.get('min_salary', 0):,} - ₹{market_data.get('max_salary', 0):,}
        
        Generate strategy with:
        1. recommended_offer: Specific salary recommendation
        2. negotiation_room: How much flexibility exists
        3. key_talking_points: List of persuasive points
        4. counter_offer_scenarios: Possible candidate responses and our replies
        5. alternative_benefits: Non-salary value propositions
        6. risk_assessment: Likelihood of acceptance
        7. fallback_options: If negotiation stalls
        
        Return as JSON.
        """
        
        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("Generated negotiation strategy")
            
            return result
            
        except Exception as e:
            logger.error(f"Negotiation strategy error: {e}")
            return {
                "recommended_offer": candidate_expectations.get('expected_salary', 0),
                "negotiation_room": "Limited data available",
                "key_talking_points": ["Competitive package", "Growth opportunities"],
                "counter_offer_scenarios": [],
                "alternative_benefits": [],
                "risk_assessment": "Medium",
                "fallback_options": ["Review budget constraints"]
            }
