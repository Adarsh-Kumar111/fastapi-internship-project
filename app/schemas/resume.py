from typing import List, Optional, Any
from datetime import datetime
from pydantic import BaseModel

class ParsedResumeData(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    professional_summary: Optional[str] = None
    technical_skills: List[str] = []
    soft_skills: List[str] = []
    education: List[str] = []
    work_experience: List[str] = []
    projects: List[str] = []
    certifications: List[str] = []
    internships: List[str] = []
    languages: List[str] = []
    achievements: List[str] = []

class ResumeResponse(BaseModel):
    id: int
    filename: str
    extracted_data: ParsedResumeData
    uploaded_at: datetime

    class Config:
        from_attributes = True