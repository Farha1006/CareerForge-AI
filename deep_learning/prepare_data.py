"""
CareerForge AI - Phase 6: Deep Learning Data Preparation Module
Script: deep_learning/prepare_data.py
Description: Loads cleaned job postings from SQLite database, applies skill multi-hot
             vectorization compatible with Phase 5 ML pipeline, and outputs PyTorch-ready
             train/test dataset tensors to deep_learning/models/.
"""

import os
import sys
import sqlite3
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder


def get_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    db_path = os.path.join(project_root, "database", "careerforge.db")
    models_dir = os.path.join(script_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    return db_path, models_dir


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


def prepare_data():
    db_path, models_dir = get_paths()

    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 6: DEEP LEARNING DATA PREPARATION", flush=True)
    print("=" * 80, flush=True)
    print(f"Loading job data from database: {db_path}", flush=True)

    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}", flush=True)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    query = """
    SELECT 
        j.job_id, 
        j.job_title, 
        GROUP_CONCAT(s.skill_name, ', ') AS skills_str 
    FROM jobs j 
    JOIN job_skills js ON j.job_id = js.job_id 
    JOIN skills s ON js.skill_id = s.skill_id 
    GROUP BY j.job_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    df['skill_list'] = df['skills_str'].apply(lambda x: [s.strip() for s in str(x).split(',') if s.strip()])
    df['target_category'] = df['job_title'].apply(categorize_title)
    df = df[df['skill_list'].map(len) > 0]

    # Vectorize using MultiLabelBinarizer & LabelEncoder (sharing schema with ML pipeline)
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(df['skill_list']).astype(np.float32)

    le = LabelEncoder()
    y = le.fit_transform(df['target_category']).astype(np.int64)

    # 80/20 Stratified Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    out_file = os.path.join(models_dir, "prepared_dl_data.npz")
    np.savez_compressed(
        out_file,
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test
    )

    # Save transformers for inference compatibility
    joblib.dump(mlb, os.path.join(models_dir, "dl_skill_mlb.joblib"))
    joblib.dump(le, os.path.join(models_dir, "dl_label_encoder.joblib"))

    print(f"\nPrepared Deep Learning Tensors:")
    print(f"  - X_train: {X_train.shape} | y_train: {y_train.shape}")
    print(f"  - X_test:  {X_test.shape}  | y_test:  {y_test.shape}")
    print(f"  - Classes ({len(le.classes_)}): {list(le.classes_)}")
    print(f"Saved dataset archive to: {out_file}")

    print("\n" + "=" * 80, flush=True)
    print("DATA PREPARATION COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    prepare_data()
