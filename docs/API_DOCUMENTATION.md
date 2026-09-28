# 🔌 REST API Documentation

---

## 1. Overview
The **CareerForge AI** backend service is implemented using **FastAPI** (`backend/app/main.py`). It serves asynchronous REST endpoints over HTTP with CORS middleware enabled for cross-origin client integration.

- **Base Server URL:** `http://localhost:8000`
- **API Router Prefix:** `/api`
- **Interactive Documentation:** `http://localhost:8000/docs` (Swagger UI) / `http://localhost:8000/redoc` (ReDoc)

---

## 2. API Endpoints Reference

### 1. Root Redirection
- **HTTP Method:** `GET`
- **Endpoint:** `/`
- **Purpose:** Redirects root HTTP requests to interactive Swagger UI documentation.
- **Request Format:** None
- **Response Format:** `307 Temporary Redirect` -> `/docs`

---

### 2. Health Check
- **HTTP Method:** `GET`
- **Endpoint:** `/api/health`
- **Purpose:** Verifies backend server health and deployment version.
- **Request Format:** None
- **Response Format (`200 OK`):**
```json
{
  "status": "healthy",
  "service": "CareerForge AI Backend API",
  "version": "1.0.0"
}
```

---

### 3. Save Student Profile
- **HTTP Method:** `POST`
- **Endpoint:** `/api/student/profile`
- **Purpose:** Accepts and validates student profile data against `StudentProfileSchema`.
- **Request Payload (`application/json`):**
```json
{
  "student_id": "STU-2026-001",
  "name": "Alex Chen",
  "education": "Undergraduate",
  "degree": "Data Science",
  "skills": ["Python", "SQL", "Excel"],
  "interests": ["Data Engineering"],
  "experience_years": 1.5,
  "preferred_location": "Remote",
  "target_career": "Data, AI & Analytics"
}
```
- **Response Format (`200 OK`):**
```json
{
  "status": "success",
  "message": "Student profile for 'Alex Chen' successfully validated and stored.",
  "data": { ... }
}
```
- **Error Response (`422 Unprocessable Entity`):** Returned if required fields (`name`, `skills`) are missing or misformatted.

---

### 4. Skill-Gap Analysis
- **HTTP Method:** `POST`
- **Endpoint:** `/api/skill-gap`
- **Purpose:** Computes matched skills, missing skills, and match percentage for a target career category.
- **Request Payload (`application/json`):**
```json
{
  "student_skills": ["Python", "SQL", "Excel"],
  "target_career": "Data, AI & Analytics"
}
```
- **Response Format (`200 OK`):**
```json
{
  "target_career": "Data, AI & Analytics",
  "skill_match_pct": 20.0,
  "matched_skills": ["SQL", "Python", "Excel"],
  "missing_skills": ["Communication", "Leadership", "AWS", "ETL", "Tableau", "R", "Agile"],
  "total_category_skills": 15
}
```

---

### 5. ML Baseline Career Prediction
- **HTTP Method:** `POST`
- **Endpoint:** `/api/predict/ml`
- **Purpose:** Predicts career category using the Phase 5 Scikit-Learn Random Forest Classifier.
- **Request Payload (`application/json`):**
```json
{
  "student_skills": ["Python", "SQL", "Pandas", "Scikit-Learn"],
  "top_k": 3
}
```
- **Response Format (`200 OK`):**
```json
{
  "predicted_category": "Data, AI & Analytics",
  "confidence": 0.427,
  "confidence_pct": 42.7,
  "top_categories": [
    { "category": "Data, AI & Analytics", "probability": 0.427, "confidence_pct": 42.7 },
    { "category": "Software & Cloud Engineering", "probability": 0.2864, "confidence_pct": 28.64 },
    { "category": "General Professional / Other", "probability": 0.2074, "confidence_pct": 20.74 }
  ],
  "top_predictions": [ ... ]
}
```

---

### 6. Deep Learning Career Prediction
- **HTTP Method:** `POST`
- **Endpoint:** `/api/predict/deep-learning`
- **Purpose:** Predicts career category using the Phase 6 PyTorch Deep Neural Network.
- **Request Payload (`application/json`):**
```json
{
  "student_skills": ["Python", "SQL", "TensorFlow", "PyTorch"],
  "top_k": 3
}
```
- **Response Format (`200 OK`):**
```json
{
  "predicted_category": "Data, AI & Analytics",
  "confidence": 0.8893,
  "confidence_pct": 88.93,
  "top_categories": [
    { "category": "Data, AI & Analytics", "probability": 0.8893, "confidence_pct": 88.93 },
    { "category": "Software & Cloud Engineering", "probability": 0.0879, "confidence_pct": 8.79 }
  ],
  "top_predictions": [ ... ]
}
```

---

### 7. Hybrid Recommendation & Learning Roadmap
- **HTTP Method:** `POST`
- **Endpoint:** `/api/recommend`
- **Purpose:** Executes the multi-criteria hybrid recommendation engine and generates a 4-stage personalized learning roadmap.
- **Request Payload (`application/json`):** `StudentProfileSchema` payload.
- **Response Format (`200 OK`):**
```json
{
  "student_profile": { ... },
  "top_ml_prediction": "Data, AI & Analytics",
  "top_dl_prediction": "Data, AI & Analytics",
  "career_recommendations": [
    {
      "career_category": "Data, AI & Analytics",
      "composite_score": 37.13,
      "is_student_target": true,
      "skill_match_pct": 13.33,
      "matched_skills": ["SQL", "Python"],
      "missing_skills": ["Communication", "Leadership", "Excel", "AWS", "ETL"],
      "ml_baseline_confidence_pct": 40.85,
      "deep_learning_confidence_pct": 88.93,
      "market_demand": {
        "total_job_listings": 1052,
        "market_share_pct": 3.16,
        "avg_annual_salary_usd": 133790.38
      }
    }
  ],
  "skill_gap": { ... },
  "market_insights": { ... },
  "learning_roadmap": [
    {
      "skill": "Communication",
      "priority": "High",
      "market_demand_pct": 48.77,
      "stage": "Stage 1: Core Foundation",
      "reason": "Essential foundational skill required in 48.8% of market job postings."
    }
  ]
}
```

---

### 8. Top Industry Demanded Skills
- **HTTP Method:** `GET`
- **Endpoint:** `/api/market/top-skills?limit=15`
- **Purpose:** Queries SQLite database for top demanded skills across all job listings.
- **Query Parameters:** `limit` (int, default=20, range: 1–100)
- **Response Format (`200 OK`):**
```json
{
  "status": "success",
  "total_skills": 15,
  "top_skills": [
    { "skill_id": 1, "skill_name": "Communication", "job_count": 16212, "percentage_of_jobs": 48.77 },
    { "skill_id": 2, "skill_name": "Leadership", "job_count": 7806, "percentage_of_jobs": 23.48 }
  ]
}
```

---

### 9. Career Categories & Market Demand
- **HTTP Method:** `GET`
- **Endpoint:** `/api/market/careers`
- **Purpose:** Returns job volume, market share %, and average salary for all 8 career categories.
- **Response Format (`200 OK`):**
```json
{
  "status": "success",
  "total_categories": 8,
  "career_categories": [
    { "career_category": "General Professional / Other", "job_count": 11326, "percentage_of_jobs": 34.07, "avg_annual_salary": 111262.15 },
    { "career_category": "Management & Operations", "job_count": 6171, "percentage_of_jobs": 18.56, "avg_annual_salary": 183849.88 },
    { "career_category": "Software & Cloud Engineering", "job_count": 4976, "percentage_of_jobs": 14.97, "avg_annual_salary": 128916.46 }
  ]
}
```

---

### 10. Geographic Job Volume Hotspots
- **HTTP Method:** `GET`
- **Endpoint:** `/api/market/locations?limit=10`
- **Purpose:** Returns job posting counts and percentages across top hiring locations.
- **Response Format (`200 OK`):**
```json
{
  "status": "success",
  "locations": [
    { "location": "United States", "job_count": 2341, "percentage_of_jobs": 7.04 },
    { "location": "New York, NY", "job_count": 818, "percentage_of_jobs": 2.46 }
  ]
}
```

---

### 11. Skill Co-occurrence Pairs
- **HTTP Method:** `GET`
- **Endpoint:** `/api/market/skill-cooccurrence?limit=10`
- **Purpose:** Returns top skill co-occurrence pairs mined from the job listings.
- **Response Format (`200 OK`):**
```json
{
  "status": "success",
  "cooccurrences": [
    { "skill_1": "Leadership", "skill_2": "Communication", "cooccurrence_count": 4808 },
    { "skill_1": "Excel", "skill_2": "Communication", "cooccurrence_count": 3574 }
  ]
}
```
