"""
CareerForge AI - Phase 4: Student Profile & Skill-Gap Analysis
Script: ml/student_profile.py
Description: Defines the StudentProfile data structure using Pydantic, supporting
             skill normalization, profile management, and serialization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class StudentProfile(BaseModel):
    """Represents a student profile for career intelligence analysis."""
    student_id: str = Field(..., description="Unique identifier for the student")
    name: str = Field(..., description="Full name of the student")
    education: str = Field("Undergraduate", description="Education level (e.g. Undergraduate, Master's)")
    degree: str = Field("Computer Science", description="Degree or major field of study")
    skills: List[str] = Field(default_factory=list, description="List of skills currently possessed")
    interests: List[str] = Field(default_factory=list, description="Career interests or domains")
    experience_years: float = Field(0.0, description="Years of professional/internship experience")
    preferred_location: str = Field("Remote", description="Preferred job location or work style")
    target_career: Optional[str] = Field(None, description="Target career role or category")

    def get_normalized_skills(self) -> set:
        """Returns a set of lowercased, whitespace-stripped skills for accurate matching."""
        return {s.strip().lower() for s in self.skills if s and s.strip()}

    def add_skill(self, new_skill: str) -> None:
        """Adds a new skill to the profile if not already present."""
        clean_skill = new_skill.strip()
        if clean_skill and clean_skill.lower() not in self.get_normalized_skills():
            self.skills.append(clean_skill)

    def remove_skill(self, skill_name: str) -> None:
        """Removes a skill from the profile."""
        norm_target = skill_name.strip().lower()
        self.skills = [s for s in self.skills if s.strip().lower() != norm_target]
