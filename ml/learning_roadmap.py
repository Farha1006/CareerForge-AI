"""
CareerForge AI - Phase 7: Personalized Learning Roadmap Generator
Script: ml/learning_roadmap.py
Description: Generates a prioritized, staged learning roadmap for a student's missing
             skills based on empirical job-market demand metrics.
"""

import os
import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional


def get_skill_market_demand(db_path: Optional[str] = None) -> Dict[str, float]:
    """Retrieves empirical skill market demand percentages from DB or top_skills.csv."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    if db_path is None:
        db_path = os.path.join(project_root, "database", "careerforge.db")

    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        total_jobs = int(pd.read_sql("SELECT COUNT(*) FROM jobs;", conn).iloc[0, 0])
        query = """
        SELECT 
            s.skill_name,
            ROUND((COUNT(js.job_id) * 100.0 / ?), 2) AS demand_pct
        FROM skills s
        JOIN job_skills js ON s.skill_id = js.skill_id
        GROUP BY s.skill_name;
        """
        df = pd.read_sql(query, conn, params=(total_jobs,))
        conn.close()
        return df.set_index('skill_name')['demand_pct'].to_dict()
    else:
        csv_path = os.path.join(project_root, "data", "processed", "analysis", "top_skills.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            return df.set_index('skill_name')['percentage_of_jobs'].to_dict()

    return {}


def generate_learning_roadmap(missing_skills: List[str], target_career: str, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Generates a personalized, 3-stage learning roadmap for a student's missing skills.
    """
    demand_dict = get_skill_market_demand(db_path)
    roadmap = []

    for skill in missing_skills:
        skill_clean = skill.strip()
        demand_pct = float(demand_dict.get(skill_clean, 2.5))  # Default 2.5% if unlisted

        # Priority categorization
        if demand_pct >= 15.0:
            priority = "High"
            stage = "Stage 1: Core Foundation"
            reason = f"Essential foundational skill required in {demand_pct:.1f}% of market job postings."
        elif demand_pct >= 5.0:
            priority = "Medium"
            stage = "Stage 2: Technical Specialization"
            reason = f"Key domain competency present in {demand_pct:.1f}% of listings for {target_career} roles."
        else:
            priority = "Standard"
            stage = "Stage 3: Advanced Mastery"
            reason = f"Specialized skill required in {demand_pct:.1f}% of advanced postings."

        roadmap.append({
            "skill": skill_clean,
            "priority": priority,
            "market_demand_pct": demand_pct,
            "stage": stage,
            "reason": reason
        })

    # Sort roadmap: Stage 1 first, then by market demand percentage descending
    stage_order = {
        "Stage 1: Core Foundation": 1,
        "Stage 2: Technical Specialization": 2,
        "Stage 3: Advanced Mastery": 3
    }
    
    roadmap.sort(key=lambda x: (stage_order.get(x["stage"], 4), -x["market_demand_pct"]))
    return roadmap
