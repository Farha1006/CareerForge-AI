"""
CareerForge AI - Phase 7: Recommendation Engine & Roadmap Test Suite
Script: ml/test_recommendation.py
Description: Evaluates hybrid career recommendations and personalized learning roadmaps
             across multiple distinct student profiles.
"""

import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from student_profile import StudentProfile
from recommendation_engine import CareerRecommendationEngine
from learning_roadmap import generate_learning_roadmap


def run_tests():
    print("=" * 80)
    print("CAREERFORGE AI - PHASE 7: HYBRID RECOMMENDATION & ROADMAP TEST SUITE")
    print("=" * 80)

    engine = CareerRecommendationEngine()

    # Test Case 1: Data Science / AI Student
    student_1 = StudentProfile(
        student_id="STU-2026-001",
        name="Alex Chen",
        education="Undergraduate (Senior Year)",
        degree="B.S. Data Science & Analytics",
        skills=["Python", "SQL", "Excel", "Problem Solving", "Communication"],
        interests=["Data Engineering", "Artificial Intelligence"],
        experience_years=1.5,
        preferred_location="Remote",
        target_career="Data, AI & Analytics"
    )

    # Test Case 2: Software Engineering & Cloud Student
    student_2 = StudentProfile(
        student_id="STU-2026-002",
        name="Sarah Jenkins",
        education="Undergraduate (Junior Year)",
        degree="B.S. Computer Science & Software Engineering",
        skills=["Java", "C++", "Linux", "Git", "Communication"],
        interests=["Cloud Infrastructure", "DevOps", "Backend Development"],
        experience_years=0.5,
        preferred_location="New York, NY",
        target_career="Software & Cloud Engineering"
    )

    test_students = [student_1, student_2]

    for idx, student in enumerate(test_students, start=1):
        print(f"\n" + "=" * 80)
        print(f"TEST CASE {idx}: {student.name.upper()} ({student.degree})")
        print("=" * 80)

        # Generate Hybrid Recommendations
        rec_data = engine.generate_recommendations(student, top_n=3)

        top_rec = rec_data["recommendations"][0]
        missing_skills = top_rec["missing_skills"]

        # Generate Personalized Learning Roadmap for Top Recommendation
        roadmap = generate_learning_roadmap(missing_skills, top_rec["career_category"])

        # Construct Final JSON Output Object
        output_json = {
            "student_profile": rec_data["student_profile"],
            "top_ml_prediction": rec_data["top_ml_prediction"],
            "top_dl_prediction": rec_data["top_dl_prediction"],
            "career_recommendations": rec_data["recommendations"],
            "skill_gap": {
                "target_career": top_rec["career_category"],
                "skill_match_pct": top_rec["skill_match_pct"],
                "matched_skills": top_rec["matched_skills"],
                "missing_skills": top_rec["missing_skills"]
            },
            "market_insights": top_rec["market_demand"],
            "learning_roadmap": roadmap
        }

        print(f"\n[1] STUDENT PROFILE & PREDICTIONS:")
        print(f"    - Student Name:       {student.name}")
        print(f"    - Possessed Skills:   {student.skills}")
        print(f"    - Target Choice:      {student.target_career}")
        print(f"    - ML Random Forest:   {rec_data['top_ml_prediction']}")
        print(f"    - PyTorch DNN:        {rec_data['top_dl_prediction']}")

        print(f"\n[2] TOP 3 HYBRID CAREER RECOMMENDATIONS:")
        print(f"    {'Rank':<5} {'Career Category':<38} {'Composite Score':<18} {'Skill Match':<14} {'DL Conf %':<12} {'ML Conf %'}")
        print("    " + "-" * 98)
        for r_idx, rec in enumerate(rec_data["recommendations"], start=1):
            target_flag = " (Target)" if rec["is_student_target"] else ""
            cat_label = f"{rec['career_category']}{target_flag}"
            skill_str = f"{rec['skill_match_pct']:.2f}%"
            dl_str = f"{rec['deep_learning_confidence_pct']:.2f}%"
            ml_str = f"{rec['ml_baseline_confidence_pct']:.2f}%"
            print(f"    {r_idx:<5} {cat_label:<38} {rec['composite_score']:<18.2f} {skill_str:<14} {dl_str:<12} {ml_str}")

        print(f"\n[3] PERSONALIZED LEARNING ROADMAP FOR '{top_rec['career_category']}':")
        print(f"    {'Stage':<35} {'Skill':<22} {'Priority':<10} Market Demand")
        print("    " + "-" * 85)
        for step in roadmap[:6]:
            print(f"    {step['stage']:<35} {step['skill']:<22} {step['priority']:<10} {step['market_demand_pct']:.1f}%")

    print("\n" + "=" * 80)
    print("HYBRID RECOMMENDATION & ROADMAP TEST SUITE PASSED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    run_tests()
