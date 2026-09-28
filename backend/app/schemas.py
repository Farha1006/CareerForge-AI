"""
CareerForge AI - FastAPI Request/Response Schemas
Script: backend/app/schemas.py
Description: Defines Pydantic data schemas for validating request payloads
             and formatting API response bodies.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class StudentProfileSchema(BaseModel):
    """Payload schema for student profiles."""
    student_id: str = Field("STU-1001", description="Unique student identifier")
    name: str = Field(..., description="Student full name")
    education: str = Field("Undergraduate", description="Educational level")
    degree: str = Field("Computer Science & Data Science", description="Degree or major field")
    skills: List[str] = Field(..., description="List of currently possessed skills")
    interests: List[str] = Field(default_factory=list, description="List of career interests")
    experience_years: float = Field(0.0, description="Years of professional/internship experience")
    preferred_location: str = Field("Remote", description="Preferred job location")
    target_career: Optional[str] = Field(None, description="Optional target career role")


class SkillGapRequest(BaseModel):
    """Payload schema for skill gap requests."""
    student_skills: List[str] = Field(..., description="List of student skills")
    target_career: str = Field(..., description="Target career domain to evaluate against")


class PredictRequest(BaseModel):
    """Payload schema for career prediction requests."""
    student_skills: List[str] = Field(..., description="List of student skills for prediction")
    top_k: Optional[int] = Field(3, description="Number of top predictions to return")


class StandardResponse(BaseModel):
    """Generic status response container."""
    status: str = "success"
    message: str
    data: Optional[Dict[str, Any]] = None
