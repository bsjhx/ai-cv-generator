from typing import List, Optional
from pydantic import BaseModel, Field

class WorkExperience(BaseModel):
    company: str
    role: str
    years: str
    description: Optional[str]=None
    skills: Optional[List[str]]=None

class Education(BaseModel):
    institution: str
    degree: str

class Project(BaseModel):
    name: str
    description: str

class UserProfile(BaseModel):
    history: List[WorkExperience]
    studies: List[Education]
    projects: List[Project]
    is_valid: bool = Field(description="False if the input is gibberish or harmful")
    missing_info: List[str] = Field(description="List of vital missing pieces")