from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    app_name: str = "User Management API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Database settings - Railway provides DATABASE_URL automatically
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/user_management")
    
    # API settings
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Security settings (for future use)
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()