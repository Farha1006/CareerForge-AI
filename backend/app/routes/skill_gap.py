"""
CareerForge AI Backend - Skill Gap Router
Script: backend/app/routes/skill_gap.py
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas import SkillGapRequest
from app.services.recommendation_service import run_skill_gap_service

router = APIRouter(prefix="/api", tags=["Skill Gap"])


@router.post("/skill-gap", status_code=status.HTTP_200_OK)
def analyze_skill_gap_endpoint(payload: SkillGapRequest):
    """
    Accepts student skills and a target career category, returning matched skills,
    missing skills, and match percentage metrics.
    """
    try:
        result = run_skill_gap_service(
            student_skills=payload.student_skills,
            target_career=payload.target_career
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Skill gap analysis failed: {str(e)}"
        )
