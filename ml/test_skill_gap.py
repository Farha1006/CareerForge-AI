"""
CareerForge AI - Phase 4: Student Profile & Skill-Gap Analysis Test Suite
Script: ml/test_skill_gap.py
Description: Demonstrates student profile instantiation, target skill-gap analysis,
             and multi-career match ranking on real job market data.
"""

import sys
import os

# Add script directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from student_profile import StudentProfile
from skill_gap import analyze_skill_gap, compare_all_careers


def run_tests():
    print("=" * 80)
    print("CAREERFORGE AI - PHASE 4: STUDENT PROFILE & SKILL-GAP TEST SUITE")
    print("=" * 80)

    # 1. Instantiate Sample Student Profile
    student = StudentProfile(
        student_id="STU-2026-001",
        name="Alex Chen",
        education="Undergraduate (Senior Year)",
        degree="B.S. Data Science & Computer Science",
        skills=["python", "sql", "excel", "problem solving", "Communication"],
        interests=["Data Engineering", "AI", "Cloud Infrastructure"],
        experience_years=1.5,
        preferred_location="Remote",
        target_career="Data, AI & Analytics"
    )

    print("\n[1/3] INSTANTIATED STUDENT PROFILE:")
    print(f"      - ID:                 {student.student_id}")
    print(f"      - Name:               {student.name}")
    print(f"      - Degree:             {student.degree}")
    print(f"      - Possessed Skills:   {student.skills}")
    print(f"      - Target Career:      {student.target_career}")

    # 2. Target Skill-Gap Analysis
    print(f"\n[2/3] RUNNING TARGET SKILL-GAP ANALYSIS FOR: '{student.target_career}'")
    gap_result = analyze_skill_gap(
        student_skills=student.skills,
        target_career=student.target_career
    )

    print(f"      - Total Industry Skills Analyzed: {gap_result['total_required']}")
    print(f"      - Matched Skills ({gap_result['matched_count']}):      {gap_result['matched_skills']}")
    print(f"      - Missing Skills ({len(gap_result['missing_skills'])}):      {gap_result['missing_skills']}")
    print(f"      - Skill Match Percentage:         {gap_result['match_percentage']}%")
    print(f"      - Skill Coverage Metric:          {gap_result['skill_coverage']}")
    print(f"      - Prioritized Learning List:     {gap_result['recommended_skills'][:5]}")

    # 3. Multi-Career Category Comparison
    print("\n[3/3] RUNNING MULTI-CAREER CATEGORY MATCH RANKING:")
    career_comparisons = compare_all_careers(student_skills=student.skills)

    print(f"      {'Rank':<5} {'Career Category':<35} {'Match %':<10} {'Matched / Total':<18} Top Missing Skill")
    print("      " + "-" * 85)

    for idx, comp in enumerate(career_comparisons, start=1):
        top_missing = comp['missing_skills'][0] if comp['missing_skills'] else 'None (100% Match)'
        matched_str = f"{len(comp['matched_skills'])} / {comp['total_required']}"
        pct_str = f"{comp['match_percentage']:.2f}%"
        print(f"      {idx:<5} {comp['target_career']:<35} {pct_str:<10} {matched_str:<18} {top_missing}")

    print("\n" + "=" * 80)
    print("TEST SUITE COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
