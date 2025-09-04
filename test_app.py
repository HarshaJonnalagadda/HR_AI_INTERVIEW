#!/usr/bin/env python3
"""
Simple test script to verify FastAPI application setup
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

async def test_imports():
    """Test that all modules can be imported successfully."""
    try:
        print("Testing imports...")
        
        # Core modules
        from core.config import settings
        from core.database import init_db
        from core.logging import setup_logging
        from core.security import create_access_token
        print("✓ Core modules imported successfully")
        
        # Models
        from models.user import User
        from models.job import Job
        from models.candidate import Candidate
        from models.interview import Interview
        print("✓ Models imported successfully")
        
        # Services
        from services.ai_service import AIService
        from services.brightdata_service import BrightDataService
        from services.outreach_service import OutreachService
        from services.calendar_service import CalendarService
        print("✓ Services imported successfully")
        
        # API endpoints
        from api.v1.endpoints import auth, jobs, candidates, interviews, dashboard, sourcing
        print("✓ API endpoints imported successfully")
        
        # Schemas
        from schemas.auth import UserLogin
        from schemas.job import JobCreate
        from schemas.candidate import CandidateCreate
        print("✓ Schemas imported successfully")
        
        # FastAPI app
        from app import app
        print("✓ FastAPI app imported successfully")
        
        print("\n🎉 All imports successful! The application is properly configured.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

async def test_config():
    """Test configuration loading."""
    try:
        from core.config import settings
        print(f"\nConfiguration test:")
        print(f"✓ App name: {settings.APP_NAME}")
        print(f"✓ Version: {settings.VERSION}")
        print(f"✓ Debug mode: {settings.DEBUG}")
        print(f"✓ Database URL configured: {'postgresql' in settings.DATABASE_URL}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

async def main():
    """Run all tests."""
    print("=" * 50)
    print("HR-AI Platform - Application Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    success &= await test_imports()
    
    # Test configuration
    success &= await test_config()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your FastAPI application is ready.")
        print("\nNext steps:")
        print("1. Set up your .env file with API keys")
        print("2. Start PostgreSQL and Redis services")
        print("3. Run: python start.py")
        print("4. Access API docs at: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    print("=" * 50)
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(asyncio.run(main()))
