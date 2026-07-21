import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartRoad AI API"
    API_V1_STR: str = "/api"
    
    # Security Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-smartroad-development-key-value-123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database Configuration (Supports fallback SQLite for local dev if Postgres is not set)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./smartroad.db"
    )

    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    class Config:
        case_sensitive = True

settings = Settings()
