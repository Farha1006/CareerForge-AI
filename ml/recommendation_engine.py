"""
CareerForge AI - Phase 7: Recommendation Engine Module
Script: ml/recommendation_engine.py
Description: Synthesizes Skill-Gap Analysis, ML Random Forest predictions, PyTorch Deep
             Learning Softmax probabilities, and Empirical Job Market Demand into a
             unified, transparent Career Recommendation Engine.
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional

# Add script directory and parent directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(script_dir)
sys.path.append(os.path.join(project_root, "deep_learning"))

from student_profile import StudentProfile
from skill_gap import analyze_skill_gap, compare_all_careers
from predict_career import predict_career_from_skills

# Import PyTorch DL Predictor safely
try:
    from predict import predict_career_dl
    HAS_DL = True
except Exception:
    HAS_DL = False


class CareerRecommendationEngine:
    """Multi-layer hybrid recommendation engine for CareerForge AI."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = os.path.join(project_root, "database", "careerforge.db")
        self.db_path = db_path
        self._load_market_stats()

    def _load_market_stats(self):
        """Loads market demand stats per career category from SQLite DB."""
        if os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            total_jobs = pd.read_sql("SELECT COUNT(*) FROM jobs;", conn).iloc[0, 0]

            query = """
            SELECT 
                job_title,
                COUNT(*) as job_count,
                AVG(annual_avg_salary) as avg_salary
            FROM jobs
            GROUP BY job_id;
            """
            df = pd.read_sql(query, conn)
            conn.close()

            def categorize_title(title):
                t = str(title).lower()
                if any(k in t for k in ['data', 'analytics', 'statistic', 'machine learning', 'ai ', 'bi ', 'business intelligence']):
                    return 'Data, AI & Analytics'
                elif any(k in t for k in ['software', 'developer', 'cloud', 'devops', 'engineer', 'systems', 'cyber', 'architect', 'network', 'it ']):
                    return 'Software & Cloud Engineering'
                elif any(k in t for k in ['sales', 'account executive', 'business development', 'marketing', 'account manager', 'commercial']):
                    return 'Sales & Marketing'
                elif any(k in t for k in ['manager', 'director', 'operations', 'project', 'product manager', 'executive', 'chief', 'head of', 'lead']):
                    return 'Management & Operations'
                elif any(k in t for k in ['accountant', 'financial', 'finance', 'controller', 'payroll', 'auditor', 'banking', 'billing']):
                    return 'Finance & Accounting'
                elif any(k in t for k in ['nurse', 'rn', 'medical', 'clinical', 'health', 'therapist', 'physician', 'dental', 'patient', 'care', 'pharmacy']):
                    return 'Healthcare & Clinical'
                elif any(k in t for k in ['customer service', 'retail', 'associate', 'cashier', 'clerk', 'receptionist', 'store', 'barista']):
                    return 'Customer Service & Retail'
                else:
                    return 'General Professional / Other'

            df['category'] = df['job_title'].apply(categorize_title)
            stats = df.groupby('category').agg(
                job_count=('job_title', 'count'),
                avg_salary=('avg_salary', 'mean')
            ).reset_index()

            stats['market_share_pct'] = (stats['job_count'] * 100.0 / total_jobs).round(2)
            self.market_stats = stats.set_index('category').to_dict('index')
        else:
            self.market_stats = {}

    def generate_recommendations(self, profile: StudentProfile, top_n: int = 5) -> Dict[str, Any]:
        """
        Generates holistic career recommendations for a student profile.
        """
        student_skills = profile.skills

        # 1. Skill Gap Analysis across all categories
        skill_gap_results = compare_all_careers(student_skills, db_path=self.db_path)

        # 2. Machine Learning Baseline Predictions
        try:
            ml_pred = predict_career_from_skills(student_skills, top_k=8)
            ml_probs = {c['category']: c['confidence_pct'] for c in ml_pred['top_categories']}
        except Exception:
            ml_pred = {"predicted_category": "N/A", "top_categories": []}
            ml_probs = {}

        # 3. Deep Learning PyTorch DNN Predictions
        if HAS_DL:
            try:
                dl_pred = predict_career_dl(student_skills, top_k=8)
                dl_probs = {c['category']: c['confidence_pct'] for c in dl_pred['top_categories']}
            except Exception:
                dl_pred = {"predicted_category": "N/A", "top_categories": []}
                dl_probs = {}
        else:
            dl_pred = {"predicted_category": "N/A", "top_categories": []}
            dl_probs = {}

        # 4. Composite Scoring Methodology
        # Composite Score = 0.40 * SkillMatch% + 0.25 * DL_Prob% + 0.20 * ML_Prob% + 0.15 * MarketShare%
        recommendations = []
        max_market_share = max([v['market_share_pct'] for v in self.market_stats.values()]) if self.market_stats else 1.0

        for item in skill_gap_results:
            cat = item['target_career']
            match_pct = item['match_percentage']

            ml_prob = ml_probs.get(cat, 0.0)
            dl_prob = dl_probs.get(cat, 0.0)

            cat_stats = self.market_stats.get(cat, {'job_count': 0, 'avg_salary': 0.0, 'market_share_pct': 0.0})
            mkt_share = cat_stats['market_share_pct']
            norm_mkt = (mkt_share / max_market_share) * 100.0 if max_market_share > 0 else 0.0

            composite_score = round(
                (0.40 * match_pct) +
                (0.25 * dl_prob) +
                (0.20 * ml_prob) +
                (0.15 * norm_mkt),
                2
            )

            is_target = (profile.target_career and profile.target_career.strip().lower() == cat.lower())

            recommendations.append({
                "career_category": cat,
                "composite_score": composite_score,
                "is_student_target": bool(is_target),
                "skill_match_pct": match_pct,
                "matched_skills": item['matched_skills'],
                "missing_skills": item['missing_skills'],
                "ml_baseline_confidence_pct": round(ml_prob, 2),
                "deep_learning_confidence_pct": round(dl_prob, 2),
                "market_demand": {
                    "total_job_listings": cat_stats['job_count'],
                    "market_share_pct": cat_stats['market_share_pct'],
                    "avg_annual_salary_usd": round(cat_stats['avg_salary'], 2) if pd.notna(cat_stats['avg_salary']) else 0.0
                }
            })

        # Sort recommendations by composite score descending
        recommendations.sort(key=lambda x: x['composite_score'], reverse=True)

        p_dict = profile.model_dump() if hasattr(profile, "model_dump") else profile.dict()
        return {
            "student_profile": p_dict,
            "top_ml_prediction": ml_pred.get("predicted_category"),
            "top_dl_prediction": dl_pred.get("predicted_category"),
            "recommendations": recommendations[:top_n]
        }
