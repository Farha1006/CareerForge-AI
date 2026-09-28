"""
CareerForge AI - Phase 6: Deep Learning Career Prediction Inference Engine
Script: deep_learning/predict.py
Description: Inference module using PyTorch Deep Neural Network to predict career categories
             and output class confidence probabilities from student skill lists.
"""

import os
import sys
import json
import joblib
import numpy as np
import torch
from typing import List, Dict, Any, Optional

from train_model import CareerDNN


class DeepLearningCareerPredictor:
    """Inference engine using PyTorch Deep Neural Network for career prediction."""

    def __init__(self, models_dir: Optional[str] = None):
        if models_dir is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            models_dir = os.path.join(script_dir, "models")

        model_path = os.path.join(models_dir, "career_dnn_model.pt")
        mlb_path = os.path.join(models_dir, "dl_skill_mlb.joblib")
        le_path = os.path.join(models_dir, "dl_label_encoder.joblib")

        if not os.path.exists(model_path) or not os.path.exists(mlb_path):
            raise FileNotFoundError(
                f"Deep Learning model artifacts missing from {models_dir}. Run prepare_data.py and train_model.py first."
            )

        self.mlb = joblib.load(mlb_path)
        self.le = joblib.load(le_path)
        self.classes = list(self.le.classes_)

        input_dim = len(self.mlb.classes_)
        num_classes = len(self.classes)

        self.model = CareerDNN(input_dim=input_dim, num_classes=num_classes)
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

    def predict(self, student_skills: List[str], top_k: int = 3) -> Dict[str, Any]:
        """
        Predicts top career categories and softmax probability confidence scores.
        """
        if not student_skills:
            return {
                "predicted_category": "General Professional / Other",
                "confidence": 0.0,
                "top_categories": [],
                "message": "No input skills provided."
            }

        clean_skills = [s.strip() for s in student_skills if s and s.strip()]
        X_vec = self.mlb.transform([clean_skills]).astype(np.float32)

        X_tensor = torch.tensor(X_vec, dtype=torch.float32)
        with torch.no_grad():
            logits = self.model(X_tensor)
            probs = torch.softmax(logits, dim=1).numpy()[0]

        ranked_indices = np.argsort(probs)[::-1]

        top_predictions = []
        for idx in ranked_indices[:top_k]:
            cat_name = self.classes[idx]
            prob_val = float(probs[idx])
            top_predictions.append({
                "category": cat_name,
                "probability": round(prob_val, 4),
                "confidence_pct": round(prob_val * 100.0, 2)
            })

        top_pred = top_predictions[0]

        return {
            "predicted_category": top_pred["category"],
            "confidence": top_pred["probability"],
            "confidence_pct": top_pred["confidence_pct"],
            "top_categories": top_predictions
        }


def predict_career_dl(student_skills: List[str], top_k: int = 3) -> Dict[str, Any]:
    predictor = DeepLearningCareerPredictor()
    return predictor.predict(student_skills, top_k=top_k)


if __name__ == "__main__":
    print("=" * 80)
    print("CAREERFORGE AI - PYTORCH DEEP LEARNING INFERENCE TEST")
    print("=" * 80)

    test_profiles = [
        {
            "name": "Data Analyst Profile",
            "skills": ["Python", "SQL", "Excel", "Tableau", "Problem Solving"]
        },
        {
            "name": "Cloud Engineer Profile",
            "skills": ["AWS", "Docker", "Kubernetes", "Linux", "Python", "CI/CD"]
        },
        {
            "name": "Healthcare & Nursing Profile",
            "skills": ["RN", "Clinical", "Patient Care", "Communication"]
        }
    ]

    predictor = DeepLearningCareerPredictor()

    for p in test_profiles:
        res = predictor.predict(p["skills"])
        print(f"\n--- {p['name']} ---")
        print(f"Input Skills:        {p['skills']}")
        print(f"Predicted Category:  {res['predicted_category']} (Confidence: {res['confidence_pct']}%)")
        print("Top 3 Predictions:")
        for rank_idx, cat_item in enumerate(res['top_categories'], start=1):
            print(f"  {rank_idx}. {cat_item['category']:<35} -> {cat_item['confidence_pct']}%")

    print("\n" + "=" * 80)
