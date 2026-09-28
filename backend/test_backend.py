"""
CareerForge AI Backend - End-to-End API Test Suite
Script: backend/test_backend.py
Description: Tests all FastAPI REST endpoints using Starlette TestClient, verifying
             HTTP status codes, schemas, and live database/model outputs.
"""

import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))

sys.path.append(script_dir)
sys.path.append(os.path.join(project_root, "ml"))
sys.path.append(os.path.join(project_root, "deep_learning"))

from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_all_endpoints():
    print("=" * 80)
    print("CAREERFORGE AI - FASTAPI BACKEND API TEST SUITE")
    print("=" * 80)

    # 1. Health Check GET /api/health
    print("\n[1/7] Testing GET /api/health...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Failed health check: {res.text}"
    print(f"      Status Code: {res.status_code} | Response: {res.json()}")

    # 2. Student Profile POST /api/student/profile
    print("\n[2/7] Testing POST /api/student/profile...")
    profile_payload = {
        "student_id": "STU-2026-999",
        "name": "Alex Chen",
        "education": "Undergraduate",
        "degree": "Data Science",
        "skills": ["Python", "SQL", "Excel"],
        "interests": ["Data Engineering"],
        "experience_years": 1.0,
        "preferred_location": "Remote",
        "target_career": "Data, AI & Analytics"
    }
    res = client.post("/api/student/profile", json=profile_payload)
    assert res.status_code == 200, f"Failed profile endpoint: {res.text}"
    print(f"      Status Code: {res.status_code} | Profile Name: {res.json()['data']['name']}")

    # 3. Skill Gap POST /api/skill-gap
    print("\n[3/7] Testing POST /api/skill-gap...")
    gap_payload = {
        "student_skills": ["Python", "SQL", "Excel"],
        "target_career": "Data, AI & Analytics"
    }
    res = client.post("/api/skill-gap", json=gap_payload)
    assert res.status_code == 200, f"Failed skill-gap endpoint: {res.text}"
    data = res.json()
    print(f"      Status Code: {res.status_code} | Target: {data['target_career']} | Match %: {data['match_percentage']}%")

    # 4. Predict ML POST /api/predict/ml
    print("\n[4/7] Testing POST /api/predict/ml...")
    pred_payload = {"student_skills": ["AWS", "Docker", "Kubernetes", "Linux"], "top_k": 3}
    res = client.post("/api/predict/ml", json=pred_payload)
    assert res.status_code == 200, f"Failed ML predict endpoint: {res.text}"
    data = res.json()
    print(f"      Status Code: {res.status_code} | ML Predicted Category: {data['predicted_category']}")

    # 5. Predict Deep Learning POST /api/predict/deep-learning
    print("\n[5/7] Testing POST /api/predict/deep-learning...")
    res = client.post("/api/predict/deep-learning", json=pred_payload)
    assert res.status_code == 200, f"Failed DL predict endpoint: {res.text}"
    data = res.json()
    print(f"      Status Code: {res.status_code} | PyTorch DL Predicted Category: {data['predicted_category']} (Conf: {data['confidence_pct']}%)")

    # 6. Market Top Skills GET /api/market/top-skills
    print("\n[6/7] Testing GET /api/market/top-skills...")
    res = client.get("/api/market/top-skills?limit=5")
    assert res.status_code == 200, f"Failed top-skills endpoint: {res.text}"
    data = res.json()
    top_skill = data['top_skills'][0]['skill_name'] if data['top_skills'] else 'N/A'
    print(f"      Status Code: {res.status_code} | Top Skill #1: {top_skill} | Returned: {len(data['top_skills'])} skills")

    # 7. Hybrid Recommendation POST /api/recommend
    print("\n[7/7] Testing POST /api/recommend...")
    res = client.post("/api/recommend", json=profile_payload)
    assert res.status_code == 200, f"Failed recommend endpoint: {res.text}"
    data = res.json()
    top_rec = data['career_recommendations'][0]['career_category']
    roadmap_len = len(data['learning_roadmap'])
    print(f"      Status Code: {res.status_code} | Top Recommendation: '{top_rec}' | Roadmap Steps: {roadmap_len}")

    print("\n" + "=" * 80)
    print("ALL 7 REST API ENDPOINTS VERIFIED AND PASSED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    test_all_endpoints()
