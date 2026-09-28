"""
CareerForge AI Backend - Market Intelligence Router
Script: backend/app/routes/market.py
"""

from fastapi import APIRouter, HTTPException, status, Query
from app.services.market_service import (
    get_top_skills_service,
    get_careers_demand_service,
    get_location_demand_service,
    get_skill_cooccurrence_service
)

router = APIRouter(prefix="/api/market", tags=["Market Intelligence"])


@router.get("/top-skills", status_code=status.HTTP_200_OK)
def get_top_skills(limit: int = Query(20, ge=1, le=100, description="Number of top skills to return")):
    """Returns top demanded skills across all job listings in the database."""
    try:
        skills = get_top_skills_service(limit=limit)
        return {
            "status": "success",
            "total_skills": len(skills),
            "top_skills": skills
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve top skills: {str(e)}"
        )


@router.get("/careers", status_code=status.HTTP_200_OK)
def get_careers_demand():
    """Returns career categories, job posting counts, market share, and average salaries."""
    try:
        careers = get_careers_demand_service()
        return {
            "status": "success",
            "total_categories": len(careers),
            "career_categories": careers
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve career demand data: {str(e)}"
        )


@router.get("/locations", status_code=status.HTTP_200_OK)
def get_location_demand(limit: int = Query(10, ge=1, le=50)):
    """Returns geographic job demand across top metropolitan regions."""
    try:
        locations = get_location_demand_service(limit=limit)
        return {
            "status": "success",
            "locations": locations
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve location demand data: {str(e)}"
        )


@router.get("/skill-cooccurrence", status_code=status.HTTP_200_OK)
def get_skill_cooccurrence(limit: int = Query(10, ge=1, le=50)):
    """Returns top skill co-occurrence pairs from data mining."""
    try:
        cooccurrences = get_skill_cooccurrence_service(limit=limit)
        return {
            "status": "success",
            "cooccurrences": cooccurrences
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve skill co-occurrences: {str(e)}"
        )
