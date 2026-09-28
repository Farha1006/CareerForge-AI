"""
CareerForge AI Backend - Health Check Router
Script: backend/app/routes/health.py
"""

from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Health"])


@router.get("/health")
def health_check():
    """Health check endpoint confirming backend server status."""
    return {
        "status": "healthy",
        "service": "CareerForge AI Backend API",
        "version": "1.0.0"
    }
