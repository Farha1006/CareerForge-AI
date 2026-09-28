"""
CareerForge AI Backend - Model Prediction Router
Script: backend/app/routes/predict.py
"""

from fastapi import APIRouter, HTTPException, status
from app.schemas import PredictRequest
from app.services.prediction_service import predict_ml_service, predict_dl_service

router = APIRouter(prefix="/api/predict", tags=["Model Predictions"])


@router.post("/ml", status_code=status.HTTP_200_OK)
def predict_ml_endpoint(payload: PredictRequest):
    """Predicts career category using the Phase 5 Random Forest ML baseline model."""
    try:
        top_k = payload.top_k if payload.top_k else 3
        res = predict_ml_service(payload.student_skills, top_k=top_k)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ML Prediction failed: {str(e)}"
        )


@router.post("/deep-learning", status_code=status.HTTP_200_OK)
def predict_dl_endpoint(payload: PredictRequest):
    """Predicts career category using the Phase 6 PyTorch Deep Neural Network."""
    try:
        top_k = payload.top_k if payload.top_k else 3
        res = predict_dl_service(payload.student_skills, top_k=top_k)
        return res
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Deep Learning Prediction failed: {str(e)}"
        )
