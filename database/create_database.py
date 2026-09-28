"""
CareerForge AI - Phase 2: Database Design & Loading
Script: database/create_database.py
Description: Creates SQLite relational database careerforge.db, creates schemas
             for jobs, skills, and job_skills tables with primary/foreign keys
             and indexes, and loads data from data/processed/jobs_cleaned.csv.
"""

import os
import sys
import sqlite3
import pandas as pd


def get_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    csv_path = os.path.join(project_root, "data", "processed", "jobs_cleaned.csv")
    db_dir = os.path.join(project_root, "database")
    db_path = os.path.join(db_dir, "careerforge.db")
    os.makedirs(db_dir, exist_ok=True)
    return csv_path, db_path


def build_database():
    csv_path, db_path = get_paths()
    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 2: DATABASE CREATION & DATA LOADING", flush=True)
    print("=" * 80, flush=True)
    print(f"Source Cleaned CSV: {csv_path}", flush=True)
    print(f"Target SQLite DB:   {db_path}", flush=True)

    if not os.path.exists(csv_path):
        print(f"Error: Processed dataset not found at {csv_path}", flush=True)
        sys.exit(1)

    # Remove existing DB file if recreating
    if os.path.exists(db_path):
        os.remove(db_path)
        print("Removed existing careerforge.db database file.", flush=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1. Create Tables
    print("\n[1/4] Creating relational schema (jobs, skills, job_skills)...", flush=True)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        job_id INTEGER PRIMARY KEY,
        company_id INTEGER,
        job_title TEXT NOT NULL,
        location TEXT,
        work_type TEXT,
        experience_level TEXT,
        posting_domain TEXT,
        remote_allowed INTEGER,
        views INTEGER,
        applies INTEGER,
        pay_period TEXT,
        currency TEXT,
        min_salary REAL,
        max_salary REAL,
        annual_min_salary REAL,
        annual_max_salary REAL,
        annual_avg_salary REAL,
        job_description TEXT,
        job_posting_url TEXT,
        listed_time REAL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_skills (
        job_id INTEGER NOT NULL,
        skill_id INTEGER NOT NULL,
        PRIMARY KEY (job_id, skill_id),
        FOREIGN KEY (job_id) REFERENCES jobs (job_id) ON DELETE CASCADE,
        FOREIGN KEY (skill_id) REFERENCES skills (skill_id) ON DELETE CASCADE
    );
    """)

    # 2. Create Indexes
    print("[2/4] Creating database indexes for optimized query performance...", flush=True)
    cursor.execute("CREATE INDEX idx_jobs_title ON jobs (job_title);")
    cursor.execute("CREATE INDEX idx_jobs_location ON jobs (location);")
    cursor.execute("CREATE INDEX idx_jobs_experience ON jobs (experience_level);")
    cursor.execute("CREATE INDEX idx_jobs_posting_domain ON jobs (posting_domain);")
    cursor.execute("CREATE INDEX idx_jobs_salary ON jobs (annual_avg_salary);")
    cursor.execute("CREATE INDEX idx_skills_name ON skills (skill_name);")
    cursor.execute("CREATE INDEX idx_job_skills_job_id ON job_skills (job_id);")
    cursor.execute("CREATE INDEX idx_job_skills_skill_id ON job_skills (skill_id);")

    # 3. Load & Transform Data into DB
    print("[3/4] Loading cleaned dataset and populating database tables...", flush=True)
    df = pd.read_csv(csv_path)

    # Insert jobs
    jobs_records = []
    for _, row in df.iterrows():
        jobs_records.append((
            int(row['job_id']),
            int(row['company_id']) if pd.notna(row['company_id']) else -1,
            str(row['clean_title']) if pd.notna(row['clean_title']) else str(row['title']),
            str(row['location']),
            str(row['formatted_work_type']),
            str(row['formatted_experience_level']),
            str(row['posting_domain']),
            int(row['remote_allowed']),
            int(row['views']),
            int(row['applies']),
            str(row['pay_period']),
            str(row['currency']),
            float(row['min_salary']) if pd.notna(row['min_salary']) else None,
            float(row['max_salary']) if pd.notna(row['max_salary']) else None,
            float(row['annual_min_salary']) if pd.notna(row['annual_min_salary']) else None,
            float(row['annual_max_salary']) if pd.notna(row['annual_max_salary']) else None,
            float(row['annual_avg_salary']) if pd.notna(row['annual_avg_salary']) else None,
            str(row['clean_description']),
            str(row['job_posting_url']),
            float(row['listed_time']) if pd.notna(row['listed_time']) else None
        ))

    cursor.executemany("""
    INSERT INTO jobs (
        job_id, company_id, job_title, location, work_type, experience_level,
        posting_domain, remote_allowed, views, applies, pay_period, currency,
        min_salary, max_salary, annual_min_salary, annual_max_salary, annual_avg_salary,
        job_description, job_posting_url, listed_time
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """, jobs_records)
    print(f"      - Inserted {len(jobs_records):,} records into 'jobs' table.", flush=True)

    # Populate normalized 'skills' table and 'job_skills' junction table
    skill_map = {}       # skill_name -> skill_id
    job_skills_records = set()  # (job_id, skill_id) tuples

    for _, row in df.iterrows():
        job_id = int(row['job_id'])
        raw_skills = row.get('cleaned_skills')
        if pd.notna(raw_skills) and str(raw_skills).strip():
            skills_list = [s.strip() for s in str(raw_skills).split(',') if s.strip()]
            for skill in skills_list:
                if skill not in skill_map:
                    cursor.execute("INSERT INTO skills (skill_name) VALUES (?);", (skill,))
                    skill_id = cursor.lastrowid
                    skill_map[skill] = skill_id
                else:
                    skill_id = skill_map[skill]

                job_skills_records.add((job_id, skill_id))

    cursor.executemany("""
    INSERT INTO job_skills (job_id, skill_id) VALUES (?, ?);
    """, list(job_skills_records))

    conn.commit()

    print(f"      - Inserted {len(skill_map):,} unique skills into 'skills' table.", flush=True)
    print(f"      - Inserted {len(job_skills_records):,} records into 'job_skills' junction table.", flush=True)

    # 4. Verification & Inspection
    print("\n[4/4] VERIFYING DATABASE CONTENTS:", flush=True)
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
    print(f"      Tables Created: {tables}", flush=True)

    print("\nTABLE RECORD COUNTS:", flush=True)
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]
        print(f"      - {table:<15}: {count:,} records", flush=True)

    print("\nSAMPLE RECORDS FROM 'jobs' TABLE (First 2):", flush=True)
    cursor.execute("SELECT job_id, job_title, location, work_type, annual_avg_salary FROM jobs LIMIT 2;")
    for r in cursor.fetchall():
        print(f"      {r}", flush=True)

    print("\nSAMPLE RECORDS FROM 'skills' TABLE (Top 5):", flush=True)
    cursor.execute("SELECT skill_id, skill_name FROM skills LIMIT 5;")
    for r in cursor.fetchall():
        print(f"      {r}", flush=True)

    print("\nSAMPLE RECORDS FROM 'job_skills' JOIN (Top 5):", flush=True)
    cursor.execute("""
    SELECT j.job_title, s.skill_name
    FROM job_skills js
    JOIN jobs j ON js.job_id = j.job_id
    JOIN skills s ON js.skill_id = s.skill_id
    LIMIT 5;
    """)
    for r in cursor.fetchall():
        print(f"      Job: '{r[0]}' <---> Skill: '{r[1]}'", flush=True)

    conn.close()
    print("\n" + "=" * 80, flush=True)
    print("DATABASE CREATION & LOADING COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    build_database()
