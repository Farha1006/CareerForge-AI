"""
CareerForge AI Backend - Recommendation Router
Script: backend/app/routes/recommend.py
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas import StudentProfileSchema
from app.services.recommendation_service import run_recommendation_service

router = APIRouter(prefix="/api", tags=["Recommendation Engine"])


@router.post("/recommend", status_code=status.HTTP_200_OK)
def get_recommendations_endpoint(profile: StudentProfileSchema):
    """
    Accepts a complete student profile and runs the multi-layer hybrid recommendation engine,
    returning career recommendations, skill gap metrics, market insights, and personalized learning roadmap.
    """
    try:
        p_dict = profile.model_dump() if hasattr(profile, "model_dump") else profile.dict()
        results = run_recommendation_service(p_dict)
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation pipeline failed: {str(e)}"
        )
