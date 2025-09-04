#!/usr/bin/env python3
"""
HR-AI Recruitment Platform Startup Script
This script initializes the database and starts the FastAPI application.
"""

import asyncio
import uvicorn
from core.database import init_db
from core.logging import setup_logging
from core.config import settings
import structlog

logger = structlog.get_logger()

async def startup():
    """Initialize the application on startup."""
    try:
        # Setup logging
        setup_logging()
        logger.info("Starting HR-AI Recruitment Platform", version=settings.VERSION)
        
        # Initialize database
        logger.info("Initializing database...")
        await init_db()
        logger.info("Database initialized successfully")
        
        return True
    except Exception as e:
        logger.error("Failed to initialize application", error=str(e))
        return False

def main():
    """Main entry point for the application."""
    # Run startup tasks
    startup_success = asyncio.run(startup())
    
    if not startup_success:
        logger.error("Application startup failed")
        return 1
    
    # Start the FastAPI server
    logger.info("Starting FastAPI server", host="0.0.0.0", port=8000)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
        access_log=True,
        workers=1 if settings.DEBUG else 4
    )

if __name__ == "__main__":
    exit(main())
