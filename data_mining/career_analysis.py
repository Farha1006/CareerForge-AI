"""
CareerForge AI - Phase 3: Data Mining
Script: data_mining/career_analysis.py
Description: Categorizes job titles into major career domains, computes domain-level
             job demand, and extracts top skills per career category.
"""

import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


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


def run_career_analysis(conn, output_dir, plots_dir):
    print("  [2/3] Running Career Category Analysis...", flush=True)

    # 1. Load jobs and categorize
    df_jobs = pd.read_sql("SELECT job_id, job_title, annual_avg_salary FROM jobs;", conn)
    df_jobs['career_category'] = df_jobs['job_title'].apply(categorize_title)

    # 2. Calculate Career Category Demand
    total_jobs = len(df_jobs)
    career_demand = df_jobs.groupby('career_category').agg(
        job_count=('job_id', 'count'),
        avg_annual_salary=('annual_avg_salary', 'mean')
    ).reset_index()

    career_demand['percentage_of_jobs'] = (career_demand['job_count'] * 100.0 / total_jobs).round(2)
    career_demand['avg_annual_salary'] = career_demand['avg_annual_salary'].round(2)
    career_demand = career_demand.sort_values(by='job_count', ascending=False)

    career_demand_path = os.path.join(output_dir, "career_demand.csv")
    career_demand.to_csv(career_demand_path, index=False)
    print(f"        -> Saved career demand to: {career_demand_path}", flush=True)

    # 3. Top Skills per Career Category
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS temp_job_categories;")
    cursor.execute("CREATE TEMP TABLE temp_job_categories (job_id INTEGER PRIMARY KEY, category TEXT);")

    cat_records = [(int(row['job_id']), row['career_category']) for _, row in df_jobs.iterrows()]
    cursor.executemany("INSERT INTO temp_job_categories VALUES (?, ?);", cat_records)

    query_career_skills = """
    SELECT 
        c.category AS career_category,
        s.skill_name,
        COUNT(js.job_id) AS skill_count
    FROM temp_job_categories c
    JOIN job_skills js ON c.job_id = js.job_id
    JOIN skills s ON js.skill_id = s.skill_id
    GROUP BY c.category, s.skill_name
    ORDER BY c.category, skill_count DESC;
    """
    df_career_skills = pd.read_sql(query_career_skills, conn)

    # Rank skills per category
    df_career_skills['rank'] = df_career_skills.groupby('career_category')['skill_count'].rank(method='first', ascending=False)
    df_top_career_skills = df_career_skills[df_career_skills['rank'] <= 10].copy()

    career_skill_path = os.path.join(output_dir, "career_skill_analysis.csv")
    df_top_career_skills.to_csv(career_skill_path, index=False)
    print(f"        -> Saved career skill analysis to: {career_skill_path}", flush=True)

    # 4. Visualizations
    # Plot 1: Career Category Job Distribution
    plt.figure(figsize=(10, 6))
    plot_df = career_demand.iloc[::-1]
    labels = list(plot_df['career_category'])
    vals = list(plot_df['job_count'])
    y_pos = list(range(len(labels)))

    plt.barh(y_pos, vals, color='#1f77b4')
    plt.yticks(y_pos, labels)
    plt.title('Job Demand Distribution by Career Category', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Job Listings', fontsize=12)
    plt.ylabel('Career Category', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plot_career_path = os.path.join(plots_dir, "career_demand.png")
    plt.savefig(plot_career_path, dpi=300)
    plt.close()

    # Plot 2: Top Skills in Data, AI & Analytics Category
    data_cat = df_top_career_skills[df_top_career_skills['career_category'] == 'Data, AI & Analytics'].head(8).iloc[::-1]
    if not data_cat.empty:
        plt.figure(figsize=(9, 5))
        d_labels = list(data_cat['skill_name'])
        d_vals = list(data_cat['skill_count'])
        d_y_pos = list(range(len(d_labels)))

        plt.barh(d_y_pos, d_vals, color='#2ca02c')
        plt.yticks(d_y_pos, d_labels)
        plt.title('Top Skills Required for Data, AI & Analytics Roles', fontsize=14, fontweight='bold')
        plt.xlabel('Demand Count', fontsize=12)
        plt.ylabel('Skill Name', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plot_data_skills_path = os.path.join(plots_dir, "data_ai_top_skills.png")
        plt.savefig(plot_data_skills_path, dpi=300)
        plt.close()

    return career_demand, df_top_career_skills
