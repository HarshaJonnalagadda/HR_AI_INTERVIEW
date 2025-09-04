from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "HR-AI Recruitment Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://username:password@localhost:5432/hr_ai_db"
    DATABASE_ECHO: bool = False
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_TEMPERATURE: float = 0.1
    
    # BrightData
    BRIGHTDATA_USERNAME: str = ""
    BRIGHTDATA_PASSWORD: str = ""
    BRIGHTDATA_ENDPOINT: str = ""
    
    # Voice Calling Configuration (Indian Providers)
    # Primary: Exotel
    EXOTEL_SID: str = ""
    EXOTEL_API_KEY: str = ""
    EXOTEL_API_TOKEN: str = ""
    EXOTEL_PHONE_NUMBER: str = ""
    
    # Alternative: Knowlarity
    KNOWLARITY_API_KEY: str = ""
    KNOWLARITY_PHONE_NUMBER: str = ""
    KNOWLARITY_CALLER_ID: str = ""
    
    # Alternative: Plivo
    PLIVO_AUTH_ID: str = ""
    PLIVO_AUTH_TOKEN: str = ""
    PLIVO_PHONE_NUMBER: str = ""
    
    # Fallback: Twilio
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    
    # Email Configuration (Gmail SMTP Primary)
    GMAIL_EMAIL: str = ""
    GMAIL_APP_PASSWORD: str = ""
    OUTLOOK_EMAIL: str = ""
    OUTLOOK_PASSWORD: str = ""
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_USE_TLS: bool = True
    
    FROM_EMAIL: str = "noreply@company.com"
    FROM_NAME: str = "HR Team"
    REPLY_TO_EMAIL: str = ""
    
    # Calendar Integration
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/google/callback"
    
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_CLIENT_SECRET: str = ""
    MICROSOFT_REDIRECT_URI: str = "http://localhost:8000/auth/microsoft/callback"
    
    # File Storage
    STORAGE_TYPE: str = "local"  # local, s3, minio
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # India Specific
    DEFAULT_TIMEZONE: str = "Asia/Kolkata"
    DEFAULT_CURRENCY: str = "INR"
    
    BRIGHTDATA_HOST: str = ""
    AUTH: str = ""
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    
    # Environment-specific settings
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Conditionally load .env file only in development
if os.getenv("ENVIRONMENT") == "production":
    # In production, rely solely on environment variables
    class ProdSettings(Settings):
        class Config:
            env_file = None
    settings = ProdSettings()
else:
    # In development, load from .env file
    settings = Settings()
