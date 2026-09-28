# CareerForge AI - ML Module: Student Profile & Skill-Gap Engine

## Overview

The `ml/` module provides a backend-independent machine learning foundation for student profile management, empirical skill-gap analysis, and multi-career compatibility scoring.

It queries the empirical job market requirements extracted during Phase 2 ([careerforge.db](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/database/careerforge.db)) and Phase 3 data mining to provide personalized career recommendations and targeted learning pathways.

---

## Core Architecture & Components

```
+--------------------------+       +------------------------------------+
|  StudentProfile Model    |       |       SkillGap Analysis Engine     |
| (ml/student_profile.py)  |       |         (ml/skill_gap.py)          |
+--------------------------+       +------------------------------------+
| - student_id, name       |       | - get_career_skill_requirements()  |
| - education, degree      |       | - analyze_skill_gap()             |
| - skills, interests      |======>| - compare_all_careers()            |
| - experience_years       |       +------------------------------------+
| - preferred_location     |                         |
| - target_career          |                         v
+--------------------------+       +------------------------------------+
                                   |       careerforge.db (SQLite)      |
                                   |  Empirical Market Skill Frequency  |
                                   +------------------------------------+
```

---

## 1. Student Profile Data Structure (`student_profile.py`)

Built using **Pydantic**, the `StudentProfile` model guarantees type validation, schema enforcement, and normalization.

### Model Attributes
* **`student_id`** (`str`): Unique identifier.
* **`name`** (`str`): Full name.
* **`education`** (`str`): Educational level (e.g., `Undergraduate`, `Master's`).
* **`degree`** (`str`): Degree/major (e.g., `Computer Science`).
* **`skills`** (`List[str]`): Currently possessed technical and soft skills.
* **`interests`** (`List[str]`): Domain interests (e.g., `Data Engineering`, `AI`).
* **`experience_years`** (`float`): Years of professional experience.
* **`preferred_location`** (`str`): Work style preference (`Remote`, `New York, NY`).
* **`target_career`** (`Optional[str]`): Optional target career role.

### Key Helper Methods
* `get_normalized_skills()`: Returns a set of lowercased, stripped skill strings for case-insensitive matching.
* `add_skill(new_skill)`: Deduplicates and appends new skills.

---

## 2. Skill-Gap & Career Comparison Engine (`skill_gap.py`)

The skill-gap engine compares a student's profile against empirical top skill requirements per career domain.

### Key Metrics Calculated

$$\text{Skill Match Percentage (\%)} = \left( \frac{|\text{Matched Skills}|}{|\text{Total Industry Required Skills}|} \right) \times 100$$

$$\text{Skill Coverage Ratio} = \frac{|\text{Matched Skills}|}{|\text{Total Industry Required Skills}|}$$

### Functions

1. **`analyze_skill_gap(student_skills, target_career, required_skills=None, db_path=None)`**:
   - Performs case-insensitive, formatting-resilient alignment between candidate skills and target career requirements.
   - Output: `matched_skills`, `missing_skills`, `match_percentage`, `skill_coverage`, and prioritized `recommended_skills`.
2. **`compare_all_careers(student_skills, db_path=None)`**:
   - Evaluates student skills across all major career categories (`Data, AI & Analytics`, `Software Engineering`, `Management & Operations`, `Sales & Marketing`, `Healthcare`, `Finance`).
   - Returns a ranked list ordered strictly by `match_percentage` descending without hard-coding preferred careers.

---

## How to Run Tests

Execute the standalone test suite to verify student profile instantiation, skill-gap calculation, and multi-career ranking:

```bash
python ml/test_skill_gap.py
```
