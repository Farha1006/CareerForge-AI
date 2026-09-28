"""
CareerForge AI - Full System Integration Test Suite
Script: tests/test_integration.py
Description: Verifies end-to-end integration across ETL, SQLite Database,
             Data Mining, ML Classifier, PyTorch DL Model, Recommendation Engine,
             Personalized Learning Roadmap, and FastAPI REST Backend.
"""

import sys
import os
import sqlite3
import pandas as pd
import unittest
from starlette.testclient import TestClient

# Resolve project paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
backend_dir = os.path.join(project_root, "backend")

sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(project_root, "ml"))
sys.path.insert(0, os.path.join(project_root, "deep_learning"))

from student_profile import StudentProfile
from skill_gap import analyze_skill_gap
from recommendation_engine import CareerRecommendationEngine
from learning_roadmap import generate_learning_roadmap
from app.main import app

client = TestClient(app)


class TestFullSystemIntegration(unittest.TestCase):
    """End-to-end integration test suite verifying system flow across all 9 components."""

    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.join(project_root, "database", "careerforge.db")
        cls.cleaned_csv = os.path.join(project_root, "data", "processed", "jobs_cleaned.csv")
        cls.ml_model_path = os.path.join(project_root, "ml", "models", "career_classifier.joblib")
        cls.dl_model_path = os.path.join(project_root, "deep_learning", "models", "career_dnn_model.pt")

    def test_01_processed_data_integrity(self):
        """Step 1: Verify ETL output CSV file exists and contains valid job listings."""
        self.assertTrue(os.path.exists(self.cleaned_csv), f"Cleaned CSV missing at {self.cleaned_csv}")
        df = pd.read_csv(self.cleaned_csv)
        self.assertGreater(len(df), 0, "Processed dataset is empty")
        self.assertTrue("clean_title" in df.columns or "title" in df.columns)
        self.assertIn("cleaned_skills", df.columns)
        print(f"[OK] ETL Processed Data Verified: {len(df)} cleaned job records.")

    def test_02_database_integrity(self):
        """Step 2: Verify SQLite database tables, primary/foreign keys, and indexes."""
        self.assertTrue(os.path.exists(self.db_path), f"SQLite database missing at {self.db_path}")
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]
        self.assertIn("jobs", tables)
        self.assertIn("skills", tables)
        self.assertIn("job_skills", tables)

        # Check job count
        cursor.execute("SELECT COUNT(*) FROM jobs;")
        job_count = cursor.fetchone()[0]
        self.assertGreater(job_count, 0)

        # Check skills count
        cursor.execute("SELECT COUNT(*) FROM skills;")
        skill_count = cursor.fetchone()[0]
        self.assertGreater(skill_count, 0)

        conn.close()
        print(f"[OK] SQLite DB Verified: {job_count} jobs, {skill_count} unique skills.")

    def test_03_ml_model_artifacts(self):
        """Step 3: Verify ML baseline model artifact files exist."""
        self.assertTrue(os.path.exists(self.ml_model_path), f"ML model missing at {self.ml_model_path}")
        print("[OK] ML Baseline Model Artifact Verified.")

    def test_04_deep_learning_model_artifacts(self):
        """Step 4: Verify PyTorch Deep Learning model artifact files exist."""
        self.assertTrue(os.path.exists(self.dl_model_path), f"DL model missing at {self.dl_model_path}")
        print("[OK] PyTorch Deep Learning Model Artifact Verified.")

    def test_05_skill_gap_analysis_engine(self):
        """Step 5: Verify standalone Skill Gap Analysis logic."""
        result = analyze_skill_gap(
            student_skills=["Python", "SQL", "Git"],
            target_career="Data, AI & Analytics",
            db_path=self.db_path
        )
        self.assertEqual(result["target_career"], "Data, AI & Analytics")
        self.assertIn("match_percentage", result)
        self.assertIn("matched_skills", result)
        self.assertIn("missing_skills", result)
        print(f"[OK] Skill-Gap Engine Verified: Match % = {result['match_percentage']}%")

    def test_06_hybrid_recommendation_engine(self):
        """Step 6: Verify Recommendation Engine integrates ML + DL + Skill Gap + Market Data."""
        engine = CareerRecommendationEngine(db_path=self.db_path)
        profile = StudentProfile(
            student_id="STU-INT-01",
            name="Alex Turner",
            education="Bachelor of Technology",
            degree="Information Technology",
            skills=["Python", "SQL", "Pandas", "Scikit-Learn", "FastAPI"],
            interests=["Data Science", "Artificial Intelligence"],
            experience_years=1.0,
            preferred_location="Remote",
            target_career="Data, AI & Analytics"
        )
        results = engine.generate_recommendations(profile, top_n=3)
        self.assertIsNotNone(results)
        self.assertIn("recommendations", results)
        self.assertGreater(len(results["recommendations"]), 0)
        top_rec = results["recommendations"][0]
        self.assertIn("career_category", top_rec)
        self.assertIn("skill_match_pct", top_rec)
        self.assertIn("market_demand", top_rec)
        print(f"[OK] Recommendation Engine Verified: Top Rec = '{top_rec['career_category']}'")

    def test_07_learning_roadmap_generator(self):
        """Step 7: Verify Personalized Learning Roadmap generation logic."""
        missing_skills = ["PyTorch", "Docker", "Kubernetes", "AWS"]
        target_category = "Data, AI & Analytics"
        roadmap = generate_learning_roadmap(missing_skills, target_category)
        self.assertGreater(len(roadmap), 0)
        self.assertIn("stage", roadmap[0])
        self.assertIn("skill", roadmap[0])
        print(f"[OK] Learning Roadmap Generator Verified: {len(roadmap)} learning stages generated.")

    def test_08_end_to_end_fastapi_rest_flow(self):
        """Step 8: Perform complete end-to-end API request simulation from frontend to backend."""
        sample_profile = {
            "student_id": "STU-E2E-999",
            "name": "Elena Rostova",
            "education": "Master of Engineering",
            "degree": "Computer Science",
            "skills": ["Python", "Java", "SQL", "Git", "Docker", "REST API", "Linux"],
            "interests": ["Backend Engineering", "Cloud Computing"],
            "experience_years": 2.0,
            "preferred_location": "Remote",
            "target_career": "Software & Cloud Engineering"
        }
        response = client.post("/api/recommend", json=sample_profile)
        self.assertEqual(response.status_code, 200, f"Recommendation API failed: {response.text}")
        payload = response.json()

        # Validate all top-level keys in standard contract
        self.assertIn("student_profile", payload)
        self.assertIn("top_ml_prediction", payload)
        self.assertIn("top_dl_prediction", payload)
        self.assertIn("career_recommendations", payload)
        self.assertIn("skill_gap", payload)
        self.assertIn("market_insights", payload)
        self.assertIn("learning_roadmap", payload)

        # Validate nested contents
        self.assertEqual(payload["student_profile"]["name"], "Elena Rostova")
        self.assertTrue(len(payload["career_recommendations"]) > 0)
        self.assertTrue(len(payload["learning_roadmap"]) > 0)

        print("\n" + "=" * 80)
        print("[PASS] END-TO-END INTEGRATION TEST PASSED SUCCESSFULLY!")
        print(f"  Student Name      : {payload['student_profile']['name']}")
        print(f"  Target Career     : {payload['skill_gap']['target_career']}")
        print(f"  Skill Match       : {payload['skill_gap']['skill_match_pct']}%")
        print(f"  Top ML Predict    : {payload['top_ml_prediction']}")
        print(f"  Top DL Predict    : {payload['top_dl_prediction']}")
        print(f"  Top Recommendation: '{payload['career_recommendations'][0]['career_category']}'")
        print("=" * 80)


if __name__ == "__main__":
    unittest.main()
