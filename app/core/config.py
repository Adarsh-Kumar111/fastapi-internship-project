import os

class Settings:
    PROJECT_NAME: str = "Internship API Portal"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-jwt-key-replace-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    PASSWORD_RESET_EXPIRE_MINUTES: int = 15     # 15 minutes
    DATABASE_URL: str = "sqlite:///./app_data.db"
    UPLOAD_DIR: str = "uploads"

settings = Settings()
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)