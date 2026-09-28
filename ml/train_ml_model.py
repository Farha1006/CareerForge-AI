"""
CareerForge AI - Phase 5: Machine Learning Baseline Training Pipeline
Script: ml/train_ml_model.py
Description: Trains a supervised classification model (Random Forest / Logistic Regression)
             to predict career categories from binary skill vectors. Saves model artifacts
             to ml/models/.
"""

import os
import sys
import json
import sqlite3
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


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


def load_and_preprocess_data(db_path):
    print("  [1/4] Loading dataset from SQLite database...", flush=True)
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

    print(f"        -> Loaded {len(df):,} job postings with associated skills.", flush=True)

    # Convert skills string to list of canonical skills per job
    df['skill_list'] = df['skills_str'].apply(lambda x: [s.strip() for s in str(x).split(',') if s.strip()])
    
    # Target variable categorization
    df['target_category'] = df['job_title'].apply(categorize_title)

    # Filter out empty skill lists if any
    df = df[df['skill_list'].map(len) > 0]

    return df


def train_pipeline():
    db_path, models_dir = get_paths()

    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 5: ML CAREER PREDICTION BASELINE TRAINING", flush=True)
    print("=" * 80, flush=True)

    if not os.path.exists(db_path):
        print(f"Error: Database file not found at {db_path}", flush=True)
        sys.exit(1)

    df = load_and_preprocess_data(db_path)

    # 2. Vectorization: Multi-Hot / Binary Skill Vector Encoding
    print("\n[2/4] Vectorizing skills using MultiLabelBinarizer...", flush=True)
    mlb = MultiLabelBinarizer()
    X = mlb.fit_transform(df['skill_list'])
    
    le = LabelEncoder()
    y = le.fit_transform(df['target_category'])

    classes = list(le.classes_)
    feature_names = list(mlb.classes_)
    print(f"      - Feature Matrix Shape: {X.shape} ({len(feature_names)} binary skill features)")
    print(f"      - Target Classes ({len(classes)}): {classes}")

    # 3. Train / Test Split
    print("\n[3/4] Performing 80/20 Stratified Train/Test Split...", flush=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"      - Training Set: {X_train.shape[0]:,} samples | Test Set: {X_test.shape[0]:,} samples")

    # 4. Model Candidate Evaluation & Training
    print("\n[4/4] Training baseline classifiers...", flush=True)

    # Model 1: Random Forest Classifier
    rf_clf = RandomForestClassifier(n_estimators=100, max_depth=25, random_state=42, n_jobs=-1)
    rf_clf.fit(X_train, y_train)
    rf_pred = rf_clf.predict(X_test)
    rf_acc = accuracy_score(y_test, rf_pred)
    rf_f1 = f1_score(y_test, rf_pred, average='weighted')
    print(f"      - Random Forest Classifier  -> Accuracy: {rf_acc*100:.2f}% | Weighted F1: {rf_f1:.4f}")

    # Model 2: Logistic Regression Classifier
    lr_clf = LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced')
    lr_clf.fit(X_train, y_train)
    lr_pred = lr_clf.predict(X_test)
    lr_acc = accuracy_score(y_test, lr_pred)
    lr_f1 = f1_score(y_test, lr_pred, average='weighted')
    print(f"      - Logistic Regression (CW) -> Accuracy: {lr_acc*100:.2f}% | Weighted F1: {lr_f1:.4f}")

    # Select best model
    if rf_f1 >= lr_f1:
        best_model = rf_clf
        best_name = "RandomForestClassifier"
        best_acc = rf_acc
        best_f1 = rf_f1
    else:
        best_model = lr_clf
        best_name = "LogisticRegression"
        best_acc = lr_acc
        best_f1 = lr_f1

    print(f"\n      -> Selected Best Model: {best_name} (F1: {best_f1:.4f})", flush=True)

    # 5. Save Artifacts to ml/models/
    model_path = os.path.join(models_dir, "career_classifier.joblib")
    mlb_path = os.path.join(models_dir, "skill_mlb.joblib")
    le_path = os.path.join(models_dir, "label_encoder.joblib")
    meta_path = os.path.join(models_dir, "model_metadata.json")

    joblib.dump(best_model, model_path)
    joblib.dump(mlb, mlb_path)
    joblib.dump(le, le_path)

    np.savez_compressed(
        os.path.join(models_dir, "test_data.npz"),
        X_test=X_test,
        y_test=y_test
    )

    metadata = {
        "model_name": best_name,
        "accuracy": round(best_acc, 4),
        "weighted_f1": round(best_f1, 4),
        "num_features": len(feature_names),
        "feature_names": feature_names,
        "classes": classes,
        "total_samples": len(df),
        "train_samples": len(X_train),
        "test_samples": len(X_test)
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSaved model artifacts to: {models_dir}")
    print(f"  - {os.path.basename(model_path)}")
    print(f"  - {os.path.basename(mlb_path)}")
    print(f"  - {os.path.basename(le_path)}")
    print(f"  - {os.path.basename(meta_path)}")

    print("\n" + "=" * 80, flush=True)
    print("TRAINING PIPELINE COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    train_pipeline()
