"""
CareerForge AI - Phase 3: Data Mining
Script: data_mining/market_analysis.py
Description: Performs market intelligence analysis analyzing job distributions by
             geographic location, industry domain, experience tier, and work type.
"""

import os
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def run_market_analysis(conn, output_dir, plots_dir):
    print("  [3/3] Running Market Intelligence Analysis...", flush=True)

    total_jobs = int(pd.read_sql("SELECT COUNT(*) FROM jobs;", conn).iloc[0, 0])

    # 1. Location Demand Analysis
    query_location = """
    SELECT 
        location,
        COUNT(*) AS job_count,
        ROUND((COUNT(*) * 100.0 / ?), 2) AS percentage_of_jobs,
        ROUND(AVG(annual_avg_salary), 2) AS avg_annual_salary
    FROM jobs
    WHERE location IS NOT NULL AND location != 'Unknown'
    GROUP BY location
    ORDER BY job_count DESC;
    """
    df_location = pd.read_sql(query_location, conn, params=(total_jobs,))
    df_location['percentage_of_jobs'] = df_location['percentage_of_jobs'].astype(float)
    location_path = os.path.join(output_dir, "location_demand.csv")
    df_location.to_csv(location_path, index=False)
    print(f"        -> Saved location demand to: {location_path}", flush=True)

    # 2. Industry / Posting Domain Demand Analysis
    query_industry = """
    SELECT 
        posting_domain AS industry_domain,
        COUNT(*) AS job_count,
        ROUND((COUNT(*) * 100.0 / ?), 2) AS percentage_of_jobs,
        ROUND(AVG(annual_avg_salary), 2) AS avg_annual_salary
    FROM jobs
    WHERE posting_domain IS NOT NULL AND posting_domain != 'Unknown'
    GROUP BY posting_domain
    ORDER BY job_count DESC;
    """
    df_industry = pd.read_sql(query_industry, conn, params=(total_jobs,))
    df_industry['percentage_of_jobs'] = df_industry['percentage_of_jobs'].astype(float)
    industry_path = os.path.join(output_dir, "industry_demand.csv")
    df_industry.to_csv(industry_path, index=False)
    print(f"        -> Saved industry domain demand to: {industry_path}", flush=True)

    # 3. Market Pattern: Salary by Experience Level
    query_exp_salary = """
    SELECT 
        experience_level,
        COUNT(*) AS total_jobs,
        ROUND(AVG(annual_avg_salary), 2) AS avg_salary,
        ROUND(MIN(annual_min_salary), 2) AS min_salary,
        ROUND(MAX(annual_max_salary), 2) AS max_salary
    FROM jobs
    WHERE experience_level IS NOT NULL AND experience_level != 'Not Specified' AND annual_avg_salary IS NOT NULL
    GROUP BY experience_level
    ORDER BY avg_salary DESC;
    """
    df_exp_salary = pd.read_sql(query_exp_salary, conn)

    # 4. Visualizations
    # Plot 1: Top 15 Locations by Demand
    plt.figure(figsize=(10, 6))
    top15_loc = df_location.head(15).iloc[::-1]
    l_labels = list(top15_loc['location'])
    l_vals = list(top15_loc['job_count'])
    l_y_pos = list(range(len(l_labels)))

    plt.barh(l_y_pos, l_vals, color='#d62728')
    plt.yticks(l_y_pos, l_labels)
    plt.title('Top 15 Job Locations by Hiring Demand', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Job Listings', fontsize=12)
    plt.ylabel('Location', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plot_loc_path = os.path.join(plots_dir, "location_demand.png")
    plt.savefig(plot_loc_path, dpi=300)
    plt.close()

    # Plot 2: Top 15 Industry Domains by Demand
    plt.figure(figsize=(10, 6))
    top15_ind = df_industry.head(15).iloc[::-1]
    i_labels = list(top15_ind['industry_domain'])
    i_vals = list(top15_ind['job_count'])
    i_y_pos = list(range(len(i_labels)))

    plt.barh(i_y_pos, i_vals, color='#9467bd')
    plt.yticks(i_y_pos, i_labels)
    plt.title('Top 15 Hiring Industry Domains', fontsize=14, fontweight='bold')
    plt.xlabel('Number of Job Listings', fontsize=12)
    plt.ylabel('Posting Domain / Industry', fontsize=12)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plot_ind_path = os.path.join(plots_dir, "industry_demand.png")
    plt.savefig(plot_ind_path, dpi=300)
    plt.close()

    # Plot 3: Salary Benchmark by Experience Level
    if not df_exp_salary.empty:
        plt.figure(figsize=(9, 5))
        plot_sal = df_exp_salary.iloc[::-1]
        s_labels = list(plot_sal['experience_level'])
        s_vals = list(plot_sal['avg_salary'])
        s_y_pos = list(range(len(s_labels)))

        plt.barh(s_y_pos, s_vals, color='#8c564b')
        plt.yticks(s_y_pos, s_labels)
        plt.title('Average Annual Salary Benchmark by Experience Level', fontsize=14, fontweight='bold')
        plt.xlabel('Average Annual Salary (USD $)', fontsize=12)
        plt.ylabel('Experience Level', fontsize=12)
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plot_sal_path = os.path.join(plots_dir, "salary_by_experience.png")
        plt.savefig(plot_sal_path, dpi=300)
        plt.close()

    return df_location, df_industry, df_exp_salary
