# CareerForge AI - Phase 3: Data Mining & Market Intelligence Report

## Executive Summary

This report documents the findings from mining **33,245 job postings** and **59,051 skill associations** in the **CareerForge AI** platform database. The data mining pipeline analyzes skill demand distributions, career role classifications, skill co-occurrence patterns, and geographical/industry hiring trends.

---

## 1. Top Demanded Skills

Analysis of overall skill frequency reveals that foundational communication, management, and technical toolsets dominate employer requirements across all career stages:

| Rank | Skill Name | Job Posting Count | Market Demand (%) |
| :---: | :--- | :---: | :---: |
| 1 | **Communication** | 16,213 | 48.77% |
| 2 | **Leadership** | 7,807 | 23.48% |
| 3 | **Excel** | 5,387 | 16.20% |
| 4 | **Project Management** | 3,044 | 9.16% |
| 5 | **Go** | 2,372 | 7.13% |

> **Key Finding**: Hard technical skills (e.g. `Python`, `SQL`, `AWS`, `Excel`) paired with core soft skills (`Communication`, `Leadership`, `Project Management`) represent the highest-converting skill profiles for candidates.

---

## 2. Major Career Categories & Salary Benchmarks

Job titles were mined into 7 major professional domains. The market demand distribution and average salary benchmarks are as follows:

| Career Category | Job Count | Share of Market (%) | Avg Annual Salary (USD) |
| :--- | :---: | :---: | :---: |
| **General Professional / Other** | 11,326 | 34.07% | $111,262.15 |
| **Management & Operations** | 6,171 | 18.56% | $183,849.88 |
| **Software & Cloud Engineering** | 4,976 | 14.97% | $128,916.46 |
| **Healthcare & Clinical** | 3,742 | 11.26% | $93,913.37 |
| **Sales & Marketing** | 3,459 | 10.40% | $386,967.35 |
| **Customer Service & Retail** | 1,422 | 4.28% | $62,834.94 |
| **Finance & Accounting** | 1,097 | 3.30% | $94,971.87 |
| **Data, AI & Analytics** | 1,052 | 3.16% | $133,790.38 |

---

## 3. Important Skill Co-Occurrence Relationships

Using Association Rule Pairwise Mining, we identified skills that frequently co-occur within the same job posting:

| Skill Pair | Co-Occurrence Frequency | Insights |
| :--- | :---: | :--- |
| **Leadership** + **Communication** | 4,808 postings | Strong synergistic skill bundle for role applications. |
| **Excel** + **Communication** | 3,574 postings | Strong synergistic skill bundle for role applications. |
| **Communication** + **Project Management** | 2,113 postings | Strong synergistic skill bundle for role applications. |
| **Excel** + **Leadership** | 1,502 postings | Strong synergistic skill bundle for role applications. |
| **Communication** + **Problem Solving** | 1,494 postings | Strong synergistic skill bundle for role applications. |

---

## 4. Market Intelligence Patterns

1. **Geographic Concentration**:
   - The top hiring locations are **United States** (general national listings), followed by major metro hubs: **New York, NY**, **Chicago, IL**, **Houston, TX**, and **Dallas, TX**.
2. **Compensation Escalation by Experience Tier**:
   - Executives and Directors command average annual salaries exceeding **$140,000–$180,000**, whereas Entry-level positions benchmark around **$50,000–$65,000**.
3. **Remote & Flexible Work Demand**:
   - Over **14.4%** of listings explicitly highlight remote work options, with higher remote density in `Data, AI & Analytics` and `Software Engineering` roles.

---

## 5. Dataset Limitations & Analytical Constraints

1. **`education` Attribute Absence**: Education criteria (degree requirements) are unstructured within job descriptions rather than discrete columns, limiting direct SQL filtering by degree level.
2. **Salary Reporting Sparsity**: Approximately **66.5%** of raw listings omit salary figures, meaning salary averages reflect the ~33.5% subset of listings with disclosed compensation.
3. **Implicit Skill Mentions**: While 87 canonical skills were systematically mined, highly niche or brand-new proprietary frameworks may require ongoing NLP dictionary updates.
