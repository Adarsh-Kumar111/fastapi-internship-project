from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl

class ProfileCreate(BaseModel):
    full_name: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    professional_summary: Optional[str] = None

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    professional_summary: Optional[str] = None

class ProfileResponse(ProfileCreate):
    id: int
    user_id: int
    updated_at: datetime

    class Config:
        from_attributes = True