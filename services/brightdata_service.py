import asyncio
import httpx
from typing import List, Dict, Optional
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class BrightDataService:
    """BrightData LinkedIn scraper service for candidate sourcing"""
    
    def __init__(self):
        self.username = settings.BRIGHTDATA_USERNAME
        self.password = settings.BRIGHTDATA_PASSWORD
        self.endpoint = settings.BRIGHTDATA_ENDPOINT
        self.session = None
    
    async def __aenter__(self):
        self.session = httpx.AsyncClient(
            auth=(self.username, self.password),
            timeout=30.0
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.aclose()
    
    async def search_linkedin_profiles(
        self, 
        keywords: List[str],
        location: str = "India",
        experience_level: str = None,
        company_size: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """Search LinkedIn profiles using BrightData"""
        
        search_params = {
            "keywords": " ".join(keywords),
            "location": location,
            "limit": limit
        }
        
        if experience_level:
            search_params["experience_level"] = experience_level
        if company_size:
            search_params["company_size"] = company_size
        
        try:
            response = await self.session.post(
                f"{self.endpoint}/linkedin/search",
                json=search_params
            )
            response.raise_for_status()
            
            profiles = response.json().get("profiles", [])
            logger.info(f"Found {len(profiles)} LinkedIn profiles")
            
            return await self._process_profiles(profiles)
            
        except httpx.HTTPError as e:
            logger.error(f"BrightData API error: {e}")
            return []
    
    async def _process_profiles(self, raw_profiles: List[Dict]) -> List[Dict]:
        """Process and clean profile data"""
        processed_profiles = []
        
        for profile in raw_profiles:
            try:
                processed_profile = {
                    "linkedin_url": profile.get("profile_url"),
                    "first_name": profile.get("first_name", "").strip(),
                    "last_name": profile.get("last_name", "").strip(),
                    "current_title": profile.get("headline", "").strip(),
                    "current_company": profile.get("current_company", "").strip(),
                    "location": profile.get("location", "").strip(),
                    "experience_years": self._extract_experience_years(profile),
                    "skills": profile.get("skills", []),
                    "education": profile.get("education", []),
                    "summary": profile.get("summary", "").strip(),
                    "profile_image": profile.get("profile_image"),
                    "connections_count": profile.get("connections_count", 0)
                }
                
                # Only add profiles with minimum required data
                if (processed_profile["first_name"] and 
                    processed_profile["last_name"] and 
                    processed_profile["linkedin_url"]):
                    processed_profiles.append(processed_profile)
                    
            except Exception as e:
                logger.warning(f"Error processing profile: {e}")
                continue
        
        return processed_profiles
    
    def _extract_experience_years(self, profile: Dict) -> Optional[int]:
        """Extract years of experience from profile data"""
        try:
            experience = profile.get("experience", [])
            if not experience:
                return None
            
            total_months = 0
            for exp in experience:
                start_date = exp.get("start_date")
                end_date = exp.get("end_date", "present")
                
                if start_date:
                    # Calculate duration (simplified)
                    if end_date == "present":
                        # Assume current year for calculation
                        duration_months = 12  # Placeholder
                    else:
                        duration_months = 12  # Placeholder calculation
                    
                    total_months += duration_months
            
            return max(1, total_months // 12)  # Convert to years
            
        except Exception:
            return None
    
    async def get_profile_details(self, linkedin_url: str) -> Optional[Dict]:
        """Get detailed profile information"""
        try:
            response = await self.session.post(
                f"{self.endpoint}/linkedin/profile",
                json={"profile_url": linkedin_url}
            )
            response.raise_for_status()
            
            return response.json()
            
        except httpx.HTTPError as e:
            logger.error(f"Error fetching profile details: {e}")
            return None
    
    async def search_by_job_requirements(
        self,
        job_title: str,
        required_skills: List[str],
        location: str = "India",
        experience_level: str = None,
        limit: int = 50
    ) -> List[Dict]:
        """Search profiles based on job requirements"""
        
        # Combine job title and skills for search
        search_keywords = [job_title] + required_skills[:5]  # Limit keywords
        
        return await self.search_linkedin_profiles(
            keywords=search_keywords,
            location=location,
            experience_level=experience_level,
            limit=limit
        )
