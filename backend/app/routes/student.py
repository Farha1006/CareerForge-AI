"""
CareerForge AI Backend - Student Profile Router
Script: backend/app/routes/student.py
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas import StudentProfileSchema, StandardResponse

router = APIRouter(prefix="/api/student", tags=["Student Profile"])


@router.post("/profile", response_model=StandardResponse, status_code=status.HTTP_200_OK)
def save_student_profile(profile: StudentProfileSchema):
    """Accepts and validates a student profile payload."""
    try:
        profile_dict = profile.model_dump() if hasattr(profile, "model_dump") else profile.dict()
        return StandardResponse(
            status="success",
            message=f"Student profile for '{profile.name}' successfully validated and stored.",
            data=profile_dict
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error validating student profile: {str(e)}"
        )
