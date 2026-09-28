"""
CareerForge AI - Phase 1: Data Engineering & Pipeline
Script: etl/01_inspect_raw_data.py
Description: Initial inspection script for the raw job postings dataset.
             Performs basic structure analysis, missing value profiling,
             and descriptive statistics without altering raw data.
"""

import os
import sys
import pandas as pd


def get_raw_data_path():
    # Resolve project root directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))

    # Check possible raw file names
    possible_files = ["raw_job_postings.csv", "job_postings.csv", "postings.csv"]
    for fname in possible_files:
        path = os.path.join(project_root, "data", "raw", fname)
        if os.path.exists(path):
            return path

    # Default fallback
    return os.path.join(project_root, "data", "raw", "raw_job_postings.csv")


def inspect_dataset():
    filepath = get_raw_data_path()
    print("=" * 80)
    print("CAREERFORGE AI - RAW DATASET INSPECTION")
    print("=" * 80)
    print(f"Loading raw dataset from: {filepath}")

    if not os.path.exists(filepath):
        print(f"Error: Raw dataset file not found at {filepath}")
        sys.exit(1)

    # 1. Load dataset
    df = pd.read_csv(filepath)

    # 2. Number of rows and columns
    rows, cols = df.shape
    print(f"\n1. DATASET SHAPE:")
    print(f"   - Total Rows:    {rows:,}")
    print(f"   - Total Columns: {cols}")

    # 3. Column names
    print(f"\n2. COLUMN NAMES ({len(df.columns)} Total):")
    for idx, col in enumerate(df.columns, start=1):
        print(f"   {idx:02d}. {col}")

    # 4. First 5 rows
    print(f"\n3. FIRST 5 ROWS:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.head(5))

    # 5. Data types
    print(f"\n4. DATA TYPES:")
    for col, dtype in df.dtypes.items():
        print(f"   - {col:<30}: {dtype}")

    # 6. Missing value counts
    print(f"\n5. MISSING VALUE COUNTS & PERCENTAGES:")
    missing = df.isnull().sum()
    missing_pct = (missing / rows) * 100
    missing_df = pd.DataFrame({
        'Missing_Count': missing,
        'Percentage (%)': missing_pct
    }).sort_values(by='Missing_Count', ascending=False)
    print(missing_df.to_string())

    # 7. Duplicate row count
    duplicates = df.duplicated().sum()
    print(f"\n6. DUPLICATE ROWS:")
    print(f"   - Total Duplicate Rows: {duplicates:,} ({(duplicates/rows)*100:.2f}%)")

    # 8. Basic statistics for relevant numerical columns
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    print(f"\n7. NUMERICAL COLUMNS DESCRIPTIVE STATISTICS:")
    if numerical_cols:
        print(df[numerical_cols].describe().T.to_string())
    else:
        print("   No numerical columns found.")

    # 9. Unique value counts for important categorical columns
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    # Filter for key categorical columns
    key_categories = [col for col in ['formatted_work_type', 'formatted_experience_level', 'pay_period', 'currency', 'work_type', 'location'] if col in df.columns]
    if not key_categories:
        key_categories = categorical_cols[:6]

    print(f"\n8. UNIQUE VALUE COUNTS FOR IMPORTANT CATEGORICAL COLUMNS:")
    for col in key_categories:
        nunique = df[col].nunique(dropna=False)
        print(f"\n   --- Unique Count for '{col}': {nunique:,} ---")
        top_vals = df[col].value_counts(dropna=False).head(10)
        print(top_vals.to_string())

    print("\n" + "=" * 80)
    print("INSPECTION COMPLETE (Raw data left intact)")
    print("=" * 80)


if __name__ == "__main__":
    inspect_dataset()
