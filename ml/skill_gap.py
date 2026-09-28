"""
CareerForge AI - Phase 4: Student Profile & Skill-Gap Analysis
Script: ml/skill_gap.py
Description: Skill-gap analysis and multi-career comparison engine utilizing
             empirical job market skill demands from database/careerforge.db.
"""

import os
import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional


def get_default_db_path() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    return os.path.join(project_root, "database", "careerforge.db")


def get_career_skill_requirements(db_path: Optional[str] = None, top_n: int = 15) -> Dict[str, List[str]]:
    """
    Fetches the top N required skills per career category directly from the database
    or saved analysis CSVs.
    """
    if db_path is None:
        db_path = get_default_db_path()

    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        # Import career category mapping function from career_analysis if temp table isn't built
        # Or run inline SQL join with title keywords
        query = """
        SELECT 
            j.job_title,
            s.skill_name
        FROM jobs j
        JOIN job_skills js ON j.job_id = js.job_id
        JOIN skills s ON js.skill_id = s.skill_id;
        """
        df_js = pd.read_sql(query, conn)
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

        df_js['career_category'] = df_js['job_title'].apply(categorize_title)
        
        # Group and rank top N skills per career category
        skill_counts = df_js.groupby(['career_category', 'skill_name']).size().reset_index(name='demand_count')
        skill_counts['rank'] = skill_counts.groupby('career_category')['demand_count'].rank(method='first', ascending=False)
        top_skills_df = skill_counts[skill_counts['rank'] <= top_n].sort_values(['career_category', 'rank'])

        career_map = {}
        for cat, group in top_skills_df.groupby('career_category'):
            career_map[cat] = group['skill_name'].tolist()

        return career_map
    else:
        # Fallback to CSV if DB not present
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.abspath(os.path.join(script_dir, "..", "data", "processed", "analysis", "career_skill_analysis.csv"))
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            career_map = {}
            for cat, group in df.groupby('career_category'):
                career_map[cat] = group.head(top_n)['skill_name'].tolist()
            return career_map

    raise FileNotFoundError("Neither careerforge.db nor career_skill_analysis.csv was found.")


def analyze_skill_gap(
    student_skills: List[str],
    target_career: str,
    required_skills: Optional[List[str]] = None,
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Performs case-insensitive skill-gap analysis comparing student skills against
    industry requirements for a target career category.
    """
    if required_skills is None:
        career_map = get_career_skill_requirements(db_path)
        required_skills = career_map.get(target_career, [])

    if not required_skills:
        return {
            'target_career': target_career,
            'matched_skills': [],
            'missing_skills': [],
            'match_percentage': 0.0,
            'skill_coverage': 0.0,
            'recommended_skills': [],
            'total_required': 0,
            'message': f"No industry requirements found for career category '{target_career}'."
        }

    # Case-insensitive skill sets
    student_skill_map = {s.strip().lower(): s.strip() for s in student_skills if s and s.strip()}
    
    matched_skills = []
    missing_skills = []

    for req_skill in required_skills:
        req_norm = req_skill.strip().lower()
        if req_norm in student_skill_map:
            matched_skills.append(req_skill)
        else:
            missing_skills.append(req_skill)

    total_req = len(required_skills)
    matched_cnt = len(matched_skills)
    
    match_pct = round((matched_cnt / total_req) * 100.0, 2) if total_req > 0 else 0.0
    coverage = round(matched_cnt / total_req, 4) if total_req > 0 else 0.0

    return {
        'target_career': target_career,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'match_percentage': match_pct,
        'skill_coverage': coverage,
        'recommended_skills': missing_skills,
        'total_required': total_req,
        'matched_count': matched_cnt
    }


def compare_all_careers(
    student_skills: List[str],
    db_path: Optional[str] = None,
    top_n_skills: int = 15
) -> List[Dict[str, Any]]:
    """
    Compares a student's skills across ALL available career categories from the dataset,
    returning results ordered by match percentage descending.
    """
    career_map = get_career_skill_requirements(db_path, top_n=top_n_skills)
    results = []

    for career_category, req_skills in career_map.items():
        analysis = analyze_skill_gap(
            student_skills=student_skills,
            target_career=career_category,
            required_skills=req_skills,
            db_path=db_path
        )
        results.append(analysis)

    # Order careers by match percentage descending
    results.sort(key=lambda x: x['match_percentage'], reverse=True)
    return results
