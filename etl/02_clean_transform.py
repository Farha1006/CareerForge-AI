"""
CareerForge AI - Phase 1B: Data Cleaning & Transformation Pipeline
Script: etl/02_clean_transform.py
Description: Reads raw dataset from data/raw/raw_job_postings.csv, applies
             text normalization, deduplication, missing-value imputation,
             salary annualization, and skill extraction, and outputs clean
             dataset to data/processed/jobs_cleaned.csv.
"""

import os
import sys
import re
import html
import pandas as pd
import numpy as np

# Standard skill dictionary for normalization and NLP extraction
CANONICAL_SKILLS = [
    "Python", "SQL", "Java", "C++", "C#", "R", "Scala", "Julia", "Go", "Rust",
    "JavaScript", "TypeScript", "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js", "Django", "Flask", "FastAPI",
    "SQLAlchemy", "PostgreSQL", "MySQL", "Oracle", "MongoDB", "Cassandra", "Redis", "Elasticsearch",
    "AWS", "Azure", "GCP", "Google Cloud", "Docker", "Kubernetes", "Terraform", "Ansible", "Linux", "Unix",
    "Spark", "PySpark", "Hadoop", "Hive", "Kafka", "Airflow", "Snowflake", "Databricks", "dbt",
    "ETL", "Data Engineering", "Data Warehouse", "Data Pipeline", "Data Mining",
    "Machine Learning", "Deep Learning", "NLP", "Natural Language Processing", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-Learn", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
    "Tableau", "Power BI", "Excel", "Looker", "BI", "Business Intelligence",
    "Git", "GitHub", "GitLab", "CI/CD", "Jira", "Agile", "Scrum", "REST API", "GraphQL",
    "Communication", "Leadership", "Project Management", "Problem Solving", "Teamwork"
]

# Map lowercased skill names to standard display casing
SKILL_CASE_MAP = {skill.lower(): skill for skill in CANONICAL_SKILLS}

# Single mega regex pattern for ultra-fast matching
SKILL_MEGA_PATTERN = re.compile(
    r'\b(' + '|'.join(re.escape(s) for s in sorted(CANONICAL_SKILLS, key=len, reverse=True)) + r')\b',
    re.IGNORECASE
)

def get_project_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    raw_path = os.path.join(project_root, "data", "raw", "raw_job_postings.csv")
    processed_dir = os.path.join(project_root, "data", "processed")
    processed_path = os.path.join(processed_dir, "jobs_cleaned.csv")
    os.makedirs(processed_dir, exist_ok=True)
    return raw_path, processed_path

def clean_html_text(text):
    """Remove HTML tags, unescape HTML entities, and normalize whitespace."""
    if not isinstance(text, str) or pd.isna(text):
        return ""
    # Unescape HTML entities (&amp;, &lt;, etc.)
    text = html.unescape(text)
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Replace multiple newlines / tabs / spaces with single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_skills_fast(text):
    """Ultra-fast skill extraction using a single compiled mega-regex pattern."""
    if not isinstance(text, str) or not text:
        return ""
    matches = SKILL_MEGA_PATTERN.findall(text)
    if not matches:
        return ""
    # Map back to canonical casing and deduplicate
    canonical_matches = sorted(list(set(SKILL_CASE_MAP[m.lower()] for m in matches if m.lower() in SKILL_CASE_MAP)))
    return ", ".join(canonical_matches)

def annualize_salary(row):
    """Calculate annualized salary range and average based on pay_period."""
    period = str(row.get('pay_period', '')).upper()
    min_sal = row.get('min_salary')
    max_sal = row.get('max_salary')

    multipliers = {
        'HOURLY': 2080,   # 40 hrs/week * 52 weeks
        'WEEKLY': 52,
        'MONTHLY': 12,
        'YEARLY': 1
    }

    mult = multipliers.get(period, np.nan)
    if pd.isna(mult):
        return pd.Series([np.nan, np.nan, np.nan], index=['annual_min_salary', 'annual_max_salary', 'annual_avg_salary'])

    ann_min = min_sal * mult if pd.notna(min_sal) else np.nan
    ann_max = max_sal * mult if pd.notna(max_sal) else np.nan

    if pd.notna(ann_min) and pd.notna(ann_max):
        ann_avg = (ann_min + ann_max) / 2.0
    elif pd.notna(ann_min):
        ann_avg = ann_min
    elif pd.notna(ann_max):
        ann_avg = ann_max
    else:
        ann_avg = np.nan

    return pd.Series([ann_min, ann_max, ann_avg], index=['annual_min_salary', 'annual_max_salary', 'annual_avg_salary'])

def run_pipeline():
    raw_path, processed_path = get_project_paths()

    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 1B: DATA CLEANING & TRANSFORMATION PIPELINE", flush=True)
    print("=" * 80, flush=True)
    print(f"Reading raw data from: {raw_path}", flush=True)

    if not os.path.exists(raw_path):
        print(f"Error: Raw dataset file not found at {raw_path}", flush=True)
        sys.exit(1)

    df_raw = pd.read_csv(raw_path)
    df = df_raw.copy()

    # --- BEFORE SUMMARY ---
    before_rows, before_cols = df.shape
    before_duplicates = df.duplicated().sum()
    before_missing = df.isnull().sum()

    print(f"\n[1/7] INITIAL DATASET LOADED:", flush=True)
    print(f"      - Rows: {before_rows:,} | Columns: {before_cols} | Exact Duplicates: {before_duplicates:,}", flush=True)

    # --- TRANSFORMATION STEP 1: Standardize Column Names ---
    df.columns = df.columns.str.lower().str.strip().str.replace(r'[\s\-]+', '_', regex=True)
    print("\n[2/7] Standardized column names to lowercase with underscores.", flush=True)

    # --- TRANSFORMATION STEP 2: Remove Exact & Key Duplicates ---
    df = df.drop_duplicates()
    if 'job_id' in df.columns:
        df = df.drop_duplicates(subset=['job_id'], keep='first')
    print(f"      - Deduplicated dataset. Remaining rows: {len(df):,}", flush=True)

    # --- TRANSFORMATION STEP 3: Remove Invalid / Unusable Records ---
    initial_cnt = len(df)
    df['title'] = df['title'].astype(str).str.strip()
    df = df[df['title'].str.len() > 0]
    df = df[df['description'].notnull() & (df['description'].astype(str).str.strip().str.len() > 0)]
    print(f"[3/7] Removed invalid records missing title/description: {initial_cnt - len(df)} rows removed.", flush=True)

    # Fix salary min/max where min > max
    if 'min_salary' in df.columns and 'max_salary' in df.columns:
        invalid_sal = df['min_salary'] > df['max_salary']
        if invalid_sal.sum() > 0:
            print(f"      - Fixing {invalid_sal.sum()} records where min_salary > max_salary...", flush=True)
            df.loc[invalid_sal, ['min_salary', 'max_salary']] = df.loc[invalid_sal, ['max_salary', 'min_salary']].values

    # --- TRANSFORMATION STEP 4: Text Fields Cleaning & Standardization ---
    print("\n[4/7] Cleaning and standardizing text fields (titles, descriptions, locations)...", flush=True)
    df['clean_title'] = df['title'].apply(clean_html_text)
    df['clean_description'] = df['description'].apply(clean_html_text)
    df['location'] = df['location'].apply(clean_html_text).replace({'': 'Unknown'})

    # --- TRANSFORMATION STEP 5: Categorical Standardizations & Imputations ---
    print("[5/7] Standardizing categorical attributes & imputing missing values...", flush=True)
    df['formatted_experience_level'] = df['formatted_experience_level'].fillna('Not Specified').astype(str).str.strip()
    df['formatted_work_type'] = df['formatted_work_type'].fillna('Unspecified').astype(str).str.strip()
    if 'work_type' in df.columns:
        df['work_type'] = df['work_type'].fillna('UNSPECIFIED').astype(str).str.strip()

    df['pay_period'] = df['pay_period'].fillna('Unspecified').astype(str).str.strip()
    df['compensation_type'] = df['compensation_type'].fillna('Unspecified').astype(str).str.strip()
    df['currency'] = df['currency'].fillna('USD').astype(str).str.strip()

    df['remote_allowed'] = df['remote_allowed'].fillna(0).astype(int)
    df['company_id'] = df['company_id'].fillna(-1).astype(int)
    df['views'] = df['views'].fillna(0).astype(int)
    df['applies'] = df['applies'].fillna(0).astype(int)
    df['posting_domain'] = df['posting_domain'].fillna('Unknown').astype(str).str.strip()

    # --- TRANSFORMATION STEP 6: Salary Annualization ---
    print("[6/7] Calculating annualized salary benchmarks (annual_min, annual_max, annual_avg)...", flush=True)
    salary_annual_df = df.apply(annualize_salary, axis=1)
    df[['annual_min_salary', 'annual_max_salary', 'annual_avg_salary']] = salary_annual_df

    # --- TRANSFORMATION STEP 7: Skill Normalization & NLP Skill Extraction ---
    print("[7/7] Performing skill standardization and NLP skill extraction...", flush=True)
    df['skills_desc'] = df['skills_desc'].apply(clean_html_text)
    combined_text = df['skills_desc'] + " " + df['clean_description']
    df['cleaned_skills'] = combined_text.apply(extract_skills_fast)

    # --- AFTER SUMMARY & SAVING ---
    after_rows, after_cols = df.shape
    after_duplicates = df.duplicated().sum()
    after_missing = df.isnull().sum()

    print("\n" + "=" * 80, flush=True)
    print("DATA CLEANING & TRANSFORMATION SUMMARY", flush=True)
    print("=" * 80, flush=True)
    print(f"BEFORE: {before_rows:,} rows, {before_cols} columns, {before_duplicates:,} duplicates", flush=True)
    print(f"AFTER:  {after_rows:,} rows, {after_cols} columns, {after_duplicates:,} duplicates", flush=True)

    print(f"\nSAVING CLEANED DATASET TO: {processed_path}", flush=True)
    df.to_csv(processed_path, index=False)
    print("Successfully saved processed dataset.", flush=True)

    # --- PRINT DETAILED COMPARISON TABLE ---
    print("\nMISSING VALUES SUMMARY COMPARISON:", flush=True)
    comp_df = pd.DataFrame({
        'Before_Missing': before_missing,
        'After_Missing': after_missing
    }).fillna(0).astype(int)
    print(comp_df.to_string(), flush=True)

    print("\nFINAL COLUMNS IN jobs_cleaned.csv:", flush=True)
    for idx, col in enumerate(df.columns, start=1):
        print(f"  {idx:02d}. {col} ({df[col].dtype})", flush=True)

    print("\n" + "=" * 80, flush=True)
    print("PIPELINE COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)

if __name__ == "__main__":
    run_pipeline()
