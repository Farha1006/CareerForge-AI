"""
CareerForge AI - Phase 3: Data Mining
Script: data_mining/skill_analysis.py
Description: Analyzes skill frequencies, percentage metrics, skill co-occurrences,
             and generates top skill and co-occurrence visualizations.
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run_skill_analysis(conn, output_dir, plots_dir):
    print("  [1/3] Running Skill Analysis...", flush=True)

    # Total jobs as python int for parameter binding
    total_jobs = int(pd.read_sql("SELECT COUNT(*) FROM jobs;", conn).iloc[0, 0])

    # 1. Top Skills Frequency & Percentage
    query_skills = """
    SELECT 
        s.skill_id,
        s.skill_name,
        COUNT(js.job_id) AS job_count,
        ROUND((COUNT(js.job_id) * 100.0 / ?), 2) AS percentage_of_jobs
    FROM skills s
    JOIN job_skills js ON s.skill_id = js.skill_id
    GROUP BY s.skill_id, s.skill_name
    ORDER BY job_count DESC;
    """
    df_top_skills = pd.read_sql(query_skills, conn, params=(total_jobs,))
    df_top_skills['percentage_of_jobs'] = df_top_skills['percentage_of_jobs'].astype(float)
    top_skills_path = os.path.join(output_dir, "top_skills.csv")
    df_top_skills.to_csv(top_skills_path, index=False)
    print(f"        -> Saved top skills to: {top_skills_path}", flush=True)

    # 2. Skill Co-occurrence Analysis (Pairwise Relationships)
    query_cooccurrence = """
    SELECT 
        s1.skill_name AS skill_1,
        s2.skill_name AS skill_2,
        COUNT(*) AS cooccurrence_count
    FROM job_skills js1
    JOIN job_skills js2 ON js1.job_id = js2.job_id AND js1.skill_id < js2.skill_id
    JOIN skills s1 ON js1.skill_id = s1.skill_id
    JOIN skills s2 ON js2.skill_id = s2.skill_id
    GROUP BY s1.skill_name, s2.skill_name
    ORDER BY cooccurrence_count DESC;
    """
    df_relationships = pd.read_sql(query_cooccurrence, conn)
    relationships_path = os.path.join(output_dir, "skill_relationships.csv")
    df_relationships.to_csv(relationships_path, index=False)
    print(f"        -> Saved skill relationships to: {relationships_path}", flush=True)

    # 3. Visualizations
    # Plot 1: Top 15 Most Demanded Skills
    plt.figure(figsize=(10, 6))
    top15 = df_top_skills.head(15).iloc[::-1]  # Reverse for ascending horizontal bar plot
    labels = list(top15['skill_name'])
    vals = list(top15['percentage_of_jobs'])
    y_pos = list(range(len(labels)))

    plt.barh(y_pos, vals, color='#2b5c8f')
    plt.yticks(y_pos, labels)
    plt.title('Top 15 Most Demanded Skills (% of Job Listings)', fontsize=14, fontweight='bold')
    plt.xlabel('Percentage of Jobs (%)', fontsize=12)
    plt.ylabel('Skill Name', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plot_top_path = os.path.join(plots_dir, "top_skills.png")
    plt.savefig(plot_top_path, dpi=300)
    plt.close()

    # Plot 2: Skill Co-occurrence Matrix Visualization
    top10_skill_names = df_top_skills.head(10)['skill_name'].tolist()
    matrix_df = pd.DataFrame(0, index=top10_skill_names, columns=top10_skill_names)

    for _, row in df_relationships.iterrows():
        s1, s2, cnt = row['skill_1'], row['skill_2'], row['cooccurrence_count']
        if s1 in top10_skill_names and s2 in top10_skill_names:
            matrix_df.loc[s1, s2] = cnt
            matrix_df.loc[s2, s1] = cnt

    plt.figure(figsize=(10, 8))
    plt.imshow(matrix_df.values, cmap='YlGnBu', interpolation='nearest')
    plt.colorbar(label='Co-occurrence Count')
    plt.xticks(range(len(top10_skill_names)), top10_skill_names, rotation=45, ha='right')
    plt.yticks(range(len(top10_skill_names)), top10_skill_names)

    # Annotate matrix values
    for i in range(len(top10_skill_names)):
        for j in range(len(top10_skill_names)):
            val = matrix_df.iloc[i, j]
            if val > 0:
                plt.text(j, i, str(val), ha='center', va='center', color='black' if val < matrix_df.values.max()/2 else 'white')

    plt.title('Top 10 Skill Co-occurrence Heatmap Matrix', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plot_cooc_path = os.path.join(plots_dir, "skill_cooccurrence.png")
    plt.savefig(plot_cooc_path, dpi=300)
    plt.close()

    return df_top_skills, df_relationships
