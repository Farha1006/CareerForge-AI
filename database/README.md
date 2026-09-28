# CareerForge AI - Database Schema & Design Documentation

## Overview

The database module of **CareerForge AI** transforms the cleaned tabular dataset ([jobs_cleaned.csv](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/data/processed/jobs_cleaned.csv)) into a normalized relational SQLite database ([careerforge.db](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/database/careerforge.db)).

The schema is designed to support downstream Data Engineering ETL pipelines, Data Mining (Skill Co-occurrence & FP-Growth), Machine Learning salary estimation, and Deep Learning semantic career recommendations.

---

## Entity-Relationship Diagram & Schema

```
+-------------------------------+       +-------------------+       +-----------------------+
|             jobs              |       |    job_skills     |       |        skills         |
+-------------------------------+       +-------------------+       +-----------------------+
| PK job_id INTEGER             |<----->| PK,FK1 job_id INT |<----->| PK skill_id INTEGER   |
|    company_id INTEGER         |       | PK,FK2 skill_id INT|       |    skill_name TEXT    |
|    job_title TEXT             |       +-------------------+       +-----------------------+
|    location TEXT              |
|    work_type TEXT             |
|    experience_level TEXT      |
|    posting_domain TEXT        |
|    remote_allowed INTEGER     |
|    views INTEGER              |
|    applies INTEGER            |
|    pay_period TEXT            |
|    currency TEXT              |
|    min_salary REAL            |
|    max_salary REAL            |
|    annual_min_salary REAL     |
|    annual_max_salary REAL     |
|    annual_avg_salary REAL     |
|    job_description TEXT       |
|    job_posting_url TEXT       |
|    listed_time REAL           |
+-------------------------------+
```

---

## Detailed Table Specifications

### 1. `jobs` Table
Stores core job posting attributes, compensation details, location, and cleaned text descriptions.

* **`job_id`** (`INTEGER`, `PRIMARY KEY`): Unique LinkedIn posting identifier.
* **`company_id`** (`INTEGER`): Identifier for the hiring company (`-1` if unlisted).
* **`job_title`** (`TEXT`, `NOT NULL`): Standardized job title.
* **`location`** (`TEXT`): Standardized job location (City, State / Country).
* **`work_type`** (`TEXT`): Employment arrangement (`Full-time`, `Contract`, `Part-time`, `Internship`, etc.).
* **`experience_level`** (`TEXT`): Experience tier (`Entry level`, `Associate`, `Mid-Senior level`, `Director`, `Executive`).
* **`posting_domain`** (`TEXT`): Industry / domain origin proxy (`careers.company.com`, `linkedin.com`, etc.).
* **`remote_allowed`** (`INTEGER`): Flag indicating remote eligibility (`1` for Remote, `0` for On-site/Hybrid).
* **`views`** (`INTEGER`): Total views on job listing.
* **`applies`** (`INTEGER`): Total application submissions recorded.
* **`pay_period`** (`TEXT`): Original compensation period (`HOURLY`, `WEEKLY`, `MONTHLY`, `YEARLY`).
* **`currency`** (`TEXT`): ISO Currency Code (`USD`).
* **`min_salary`** (`REAL`): Minimum reported base compensation.
* **`max_salary`** (`REAL`): Maximum reported base compensation.
* **`annual_min_salary`** (`REAL`): Annualized minimum salary benchmark.
* **`annual_max_salary`** (`REAL`): Annualized maximum salary benchmark.
* **`annual_avg_salary`** (`REAL`): Annualized average salary benchmark.
* **`job_description`** (`TEXT`): Cleaned full-text job description.
* **`job_posting_url`** (`TEXT`): Canonical URL to online job posting.
* **`listed_time`** (`REAL`): Epoch timestamp of job posting creation.

---

### 2. `skills` Table
Stores a unique canonical dictionary of technical and soft skills extracted from job listings.

* **`skill_id`** (`INTEGER`, `PRIMARY KEY`, `AUTOINCREMENT`): Auto-generated unique skill identifier.
* **`skill_name`** (`TEXT`, `UNIQUE`, `NOT NULL`): Standardized canonical skill name (e.g. `Python`, `SQL`, `AWS`, `Data Engineering`).

---

### 3. `job_skills` Junction Table
Implements a normalized Many-to-Many ($M:N$) relationship linking job postings to required skills.

* **`job_id`** (`INTEGER`, `FOREIGN KEY`): References `jobs(job_id)` ON DELETE CASCADE.
* **`skill_id`** (`INTEGER`, `FOREIGN KEY`): References `skills(skill_id)` ON DELETE CASCADE.
* **`PRIMARY KEY`** (`job_id`, `skill_id`): Guarantees uniqueness per job-skill pair.

---

## Database Indexes

The schema creates dedicated B-tree indexes to accelerate analytical queries across platform features:

1. `idx_jobs_title`: Optimized for job role search and title normalization matching.
2. `idx_jobs_location`: Accelerates location-based market analytics and salary filtering.
3. `idx_jobs_experience`: Enables fast skill gap profiling by career stage (Entry vs. Senior).
4. `idx_jobs_posting_domain`: Accelerates industry and company-domain analytical aggregations.
5. `idx_jobs_salary`: Speeds up salary range distribution models and compensation queries.
6. `idx_skills_name`: Supports fast skill lookups during user resume skill extraction.
7. `idx_job_skills_job_id` & `idx_job_skills_skill_id`: Optimizes multi-table joins for skill co-occurrence mining (Apriori / FP-Growth).

---

## Design Assumptions & Adaptations

1. **`education` Attribute Adaptation**: The dataset does not contain an isolated `education` column. Education requirements (e.g., Bachelor's, Master's, Ph.D.) are embedded within the unstructured `job_description` field. We retain the full cleaned description in `job_description` to allow downstream NLP extraction without adding artificial null columns.
2. **`industry` / `posting_domain` Alignment**: Raw company industry tables are decoupled in the raw source; `posting_domain` serves as a direct proxy for industry / corporate domain origin in the core table.
3. **Skill Normalization**: Instead of duplicating skill strings per job posting, skills are extracted, mapped to canonical display titles, and stored uniquely in `skills` to ensure 3NF database normalization.

---

## Recreating the Database

To create or rebuild the SQLite database from the cleaned dataset, run:

```bash
python database/create_database.py
```

This script will automatically:
1. Re-initialize `database/careerforge.db`.
2. Construct tables with strict foreign key constraints and primary keys.
3. Build B-tree performance indexes.
4. Populate `jobs`, `skills`, and `job_skills` tables from `data/processed/jobs_cleaned.csv`.
5. Execute verification queries and report record counts.
