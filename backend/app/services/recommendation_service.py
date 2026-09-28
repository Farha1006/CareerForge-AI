"""
CareerForge AI Backend - Recommendation Service
Script: backend/app/services/recommendation_service.py
Description: Service wrapper connecting FastAPI endpoints to the recommendation engine,
             skill gap analyzer, and personalized learning roadmap generator.
"""

import os
import sys

# Resolve paths to ml and deep_learning modules
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))

sys.path.append(os.path.join(project_root, "ml"))
sys.path.append(os.path.join(project_root, "deep_learning"))

from student_profile import StudentProfile
from recommendation_engine import CareerRecommendationEngine
from learning_roadmap import generate_learning_roadmap
from skill_gap import analyze_skill_gap

# Instantiate single global recommendation engine
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        db_path = os.path.join(project_root, "database", "careerforge.db")
        _engine = CareerRecommendationEngine(db_path=db_path)
    return _engine


def run_skill_gap_service(student_skills: list, target_career: str) -> dict:
    db_path = os.path.join(project_root, "database", "careerforge.db")
    return analyze_skill_gap(
        student_skills=student_skills,
        target_career=target_career,
        db_path=db_path
    )


def run_recommendation_service(profile_data: dict, top_n: int = 5) -> dict:
    engine = get_engine()
    
    # Map dict payload to StudentProfile object
    profile = StudentProfile(**profile_data)
    rec_results = engine.generate_recommendations(profile, top_n=top_n)

    top_rec = rec_results["recommendations"][0] if rec_results["recommendations"] else None

    if top_rec:
        missing_skills = top_rec["missing_skills"]
        target_cat = top_rec["career_category"]
        roadmap = generate_learning_roadmap(missing_skills, target_cat)
    else:
        roadmap = []

    return {
        "student_profile": rec_results["student_profile"],
        "top_ml_prediction": rec_results["top_ml_prediction"],
        "top_dl_prediction": rec_results["top_dl_prediction"],
        "career_recommendations": rec_results["recommendations"],
        "skill_gap": {
            "target_career": top_rec["career_category"] if top_rec else "N/A",
            "skill_match_pct": top_rec["skill_match_pct"] if top_rec else 0.0,
            "matched_skills": top_rec["matched_skills"] if top_rec else [],
            "missing_skills": top_rec["missing_skills"] if top_rec else []
        },
        "market_insights": top_rec["market_demand"] if top_rec else {},
        "learning_roadmap": roadmap
    }
