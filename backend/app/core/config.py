from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TechStep API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "TechStep - Interactive Cybersecurity Training Platform API"
    
    # Database
    DATABASE_URL: str = "sqlite:///./techstep.db"
    
    # Security
    SECRET_KEY: str = "techstep-super-secret-key-for-development-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000", 
        "http://localhost:8080", 
        "http://localhost:5000",
        "https://localhost:3000",
        "https://localhost:8080",
        "https://localhost:5000"
    ]
    
    # Payment
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_placeholder"
    STRIPE_SECRET_KEY: str = "sk_test_placeholder"
    PAYPAL_CLIENT_ID: str = "paypal_client_id_placeholder"
    PAYPAL_CLIENT_SECRET: str = "paypal_client_secret_placeholder"
    PAYPAL_MODE: str = "sandbox"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "placeholder@gmail.com"
    SMTP_PASSWORD: str = "placeholder"
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = "placeholder"
    AWS_SECRET_ACCESS_KEY: str = "placeholder"
    AWS_S3_BUCKET: str = "techstep-uploads"
    AWS_REGION: str = "us-east-1"
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()