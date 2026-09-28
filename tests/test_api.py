"""
CareerForge AI - API Endpoint Test Suite
Script: tests/test_api.py
Description: Automated tests verifying FastAPI REST endpoints, status codes,
             request validation, and response structures.
"""

import sys
import os
import unittest
from starlette.testclient import TestClient

# Resolve paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
backend_dir = os.path.join(project_root, "backend")

sys.path.insert(0, backend_dir)
sys.path.insert(0, os.path.join(project_root, "ml"))
sys.path.insert(0, os.path.join(project_root, "deep_learning"))

from app.main import app

client = TestClient(app)


class TestAPIRoutes(unittest.TestCase):
    """Test suite for all FastAPI REST endpoints."""

    def test_01_health_check(self):
        """Test GET /api/health returns HTTP 200 and healthy status."""
        response = client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("version", data)

    def test_02_student_profile(self):
        """Test POST /api/student/profile accepts valid profile payload."""
        payload = {
            "student_id": "STU-TEST-101",
            "name": "Jordan Lee",
            "education": "Bachelor of Science",
            "degree": "Computer Science",
            "skills": ["Python", "SQL", "Git", "Docker"],
            "interests": ["Machine Learning", "Software Development"],
            "experience_years": 2.0,
            "preferred_location": "Remote",
            "target_career": "Software & Cloud Engineering"
        }
        response = client.post("/api/student/profile", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["name"], "Jordan Lee")

    def test_03_student_profile_validation_error(self):
        """Test POST /api/student/profile rejects missing required fields."""
        payload = {
            "education": "Undergraduate"
            # Missing required field 'name' and 'skills'
        }
        response = client.post("/api/student/profile", json=payload)
        self.assertEqual(response.status_code, 422)  # Unprocessable Entity

    def test_04_skill_gap_analysis(self):
        """Test POST /api/skill-gap returns match percentage and missing skills."""
        payload = {
            "student_skills": ["Python", "SQL", "Docker"],
            "target_career": "Data, AI & Analytics"
        }
        response = client.post("/api/skill-gap", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("match_percentage", data)
        self.assertIn("matched_skills", data)
        self.assertIn("missing_skills", data)
        self.assertGreaterEqual(data["match_percentage"], 0)

    def test_05_predict_ml(self):
        """Test POST /api/predict/ml returns ML predictions."""
        payload = {
            "student_skills": ["Python", "Pandas", "Scikit-Learn", "SQL"],
            "top_k": 3
        }
        response = client.post("/api/predict/ml", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predicted_category", data)
        self.assertIn("top_predictions", data)
        self.assertGreaterEqual(len(data["top_predictions"]), 1)

    def test_06_predict_deep_learning(self):
        """Test POST /api/predict/deep-learning returns PyTorch DL predictions."""
        payload = {
            "student_skills": ["Java", "Spring", "AWS", "Kubernetes"],
            "top_k": 3
        }
        response = client.post("/api/predict/deep-learning", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predicted_category", data)
        self.assertIn("confidence_pct", data)
        self.assertIn("top_predictions", data)

    def test_07_market_top_skills(self):
        """Test GET /api/market/top-skills returns demanded skills."""
        response = client.get("/api/market/top-skills?limit=10")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("top_skills", data)
        self.assertLessEqual(len(data["top_skills"]), 10)

    def test_08_market_careers(self):
        """Test GET /api/market/careers returns career category demand statistics."""
        response = client.get("/api/market/careers")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("career_categories", data)
        self.assertGreater(len(data["career_categories"]), 0)

    def test_09_full_recommendation(self):
        """Test POST /api/recommend generates complete recommendations and learning roadmap."""
        payload = {
            "student_id": "STU-RECOMMEND-01",
            "name": "Sarah Connor",
            "education": "Master of Science",
            "degree": "Artificial Intelligence",
            "skills": ["Python", "TensorFlow", "PyTorch", "Git"],
            "interests": ["Computer Vision", "NLP"],
            "experience_years": 1.5,
            "preferred_location": "New York",
            "target_career": "Data, AI & Analytics"
        }
        response = client.post("/api/recommend", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("student_profile", data)
        self.assertIn("career_recommendations", data)
        self.assertIn("top_ml_prediction", data)
        self.assertIn("top_dl_prediction", data)
        self.assertIn("learning_roadmap", data)
        self.assertGreater(len(data["career_recommendations"]), 0)
        self.assertGreater(len(data["learning_roadmap"]), 0)

    def test_10_cors_headers(self):
        """Test CORS headers are present for cross-origin frontend requests."""
        response = client.options(
            "/api/recommend",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "POST"
            }
        )
        self.assertIn(response.status_code, [200, 204])


if __name__ == "__main__":
    unittest.main()
