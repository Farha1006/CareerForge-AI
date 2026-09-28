"""
CareerForge AI Backend - Prediction Service
Script: backend/app/services/prediction_service.py
Description: Service wrapper connecting API endpoints to Phase 5 ML Random Forest
             and Phase 6 PyTorch Deep Learning classifiers.
"""

import os
import sys
from typing import List, Dict, Any

# Resolve paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

sys.path.append(os.path.join(project_root, "ml"))
sys.path.append(os.path.join(project_root, "deep_learning"))

from predict_career import predict_career_from_skills

try:
    from predict import predict_career_dl
    HAS_DL = True
except Exception:
    HAS_DL = False


def predict_ml_service(student_skills: List[str], top_k: int = 3) -> Dict[str, Any]:
    """Runs ML Random Forest prediction."""
    res = predict_career_from_skills(student_skills=student_skills, top_k=top_k)
    res["top_predictions"] = res.get("top_categories", [])
    return res


def predict_dl_service(student_skills: List[str], top_k: int = 3) -> Dict[str, Any]:
    """Runs PyTorch Deep Learning DNN prediction."""
    if not HAS_DL:
        return {
            "predicted_category": "N/A",
            "confidence": 0.0,
            "top_categories": [],
            "top_predictions": [],
            "message": "PyTorch Deep Learning engine not available."
        }
    res = predict_career_dl(student_skills=student_skills, top_k=top_k)
    res["top_predictions"] = res.get("top_categories", [])
    return res
