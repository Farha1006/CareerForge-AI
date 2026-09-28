"""
CareerForge AI Backend - Market Intelligence Service
Script: backend/app/services/market_service.py
Description: Service wrapper querying SQLite database and Phase 3 Data Mining outputs
             for top skills and career demand distributions.
"""

import os
import sqlite3
import pandas as pd
from typing import List, Dict, Any

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))


def get_top_skills_service(limit: int = 20) -> List[Dict[str, Any]]:
    db_path = os.path.join(project_root, "database", "careerforge.db")

    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        total_jobs = int(pd.read_sql("SELECT COUNT(*) FROM jobs;", conn).iloc[0, 0])
        query = """
        SELECT 
            s.skill_id,
            s.skill_name,
            COUNT(js.job_id) AS job_count,
            ROUND((COUNT(js.job_id) * 100.0 / ?), 2) AS percentage_of_jobs
        FROM skills s
        JOIN job_skills js ON s.skill_id = js.skill_id
        GROUP BY s.skill_id, s.skill_name
        ORDER BY job_count DESC
        LIMIT ?;
        """
        df = pd.read_sql(query, conn, params=(total_jobs, limit))
        conn.close()
        return df.to_dict("records")
    else:
        csv_path = os.path.join(project_root, "data", "processed", "analysis", "top_skills.csv")
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path).head(limit)
            return df.to_dict("records")

    return []


def get_careers_demand_service() -> List[Dict[str, Any]]:
    csv_path = os.path.join(project_root, "data", "processed", "analysis", "career_demand.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        return df.to_dict("records")

    db_path = os.path.join(project_root, "database", "careerforge.db")
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        df_jobs = pd.read_sql("SELECT job_id, job_title, annual_avg_salary FROM jobs;", conn)
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

        df_jobs['career_category'] = df_jobs['job_title'].apply(categorize_title)
        total_jobs = len(df_jobs)
        res = df_jobs.groupby('career_category').agg(
            job_count=('job_id', 'count'),
            avg_annual_salary=('annual_avg_salary', 'mean')
        ).reset_index()

        res['percentage_of_jobs'] = (res['job_count'] * 100.0 / total_jobs).round(2)
        res['avg_annual_salary'] = res['avg_annual_salary'].round(2)
        res = res.sort_values(by='job_count', ascending=False)
        return res.to_dict("records")

    return []


def get_location_demand_service(limit: int = 10) -> List[Dict[str, Any]]:
    """Returns location demand metrics from Phase 3 Data Mining outputs."""
    csv_path = os.path.join(project_root, "data", "processed", "analysis", "location_demand.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path).head(limit)
        return df.to_dict("records")
    return []


def get_skill_cooccurrence_service(limit: int = 10) -> List[Dict[str, Any]]:
    """Returns skill co-occurrence relationships from Phase 3 Data Mining outputs."""
    csv_path = os.path.join(project_root, "data", "processed", "analysis", "skill_relationships.csv")
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path).head(limit)
        return df.to_dict("records")
    return []
