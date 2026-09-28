# CareerForge AI - FastAPI REST API Backend

## Overview

The `backend/` directory houses the REST API for **CareerForge AI**, built using **FastAPI**, **Pydantic**, and **Uvicorn**.

It exposes the data engineering, data mining, machine learning baseline, PyTorch deep learning neural network, and personalized recommendation engine through clean RESTful JSON endpoints.

---

## Installation & Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start the FastAPI Uvicorn Server**:
   ```bash
   python -m uvicorn app.main:app --reload --port 8000
   ```

4. **Access Interactive API Documentation**:
   - **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Available API Endpoints

### 1. System Health
* **`GET /api/health`**: Returns system health status.

### 2. Student Profile
* **`POST /api/student/profile`**: Accepts and validates student profile JSON payloads.

### 3. Skill-Gap Analysis
* **`POST /api/skill-gap`**: Analyzes skill alignment between candidate skills and a target career role.

### 4. Recommendation Engine
* **`POST /api/recommend`**: Runs the hybrid recommendation engine combining Skill-Gap, PyTorch DNN, Random Forest ML, and Market Intelligence into a composite score and 3-stage learning roadmap.

### 5. Model Predictions
* **`POST /api/predict/ml`**: Predicts career categories using the Phase 5 Random Forest ML model.
* **`POST /api/predict/deep-learning`**: Predicts career categories using the Phase 6 PyTorch Deep Neural Network.

### 6. Market Intelligence
* **`GET /api/market/top-skills`**: Retrieves top demanded skills across all job listings.
* **`GET /api/market/careers`**: Retrieves career categories, job volume counts, market share %, and average annual salaries.

---

## Example API Requests & Responses

### Example 1: Skill Gap Request (`POST /api/skill-gap`)

**Request**:
```json
{
  "student_skills": ["Python", "SQL", "Excel"],
  "target_career": "Data, AI & Analytics"
}
```

**Response**:
```json
{
  "target_career": "Data, AI & Analytics",
  "matched_skills": ["SQL", "Python", "Excel"],
  "missing_skills": ["Communication", "Leadership", "AWS", "ETL", "Machine Learning"],
  "match_percentage": 20.0,
  "skill_coverage": 0.2,
  "total_required": 15
}
```

---

### Example 2: Career Recommendation (`POST /api/recommend`)

**Request**:
```json
{
  "student_id": "STU-1001",
  "name": "Alex Chen",
  "education": "Undergraduate",
  "degree": "Data Science",
  "skills": ["Python", "SQL", "Excel", "Problem Solving", "Communication"],
  "interests": ["Data Engineering"],
  "experience_years": 1.5,
  "preferred_location": "Remote",
  "target_career": "Data, AI & Analytics"
}
```

**Response**:
```json
{
  "student_profile": { ... },
  "top_ml_prediction": "Software & Cloud Engineering",
  "top_dl_prediction": "Software & Cloud Engineering",
  "career_recommendations": [
    {
      "career_category": "General Professional / Other",
      "composite_score": 37.48,
      "skill_match_pct": 33.33,
      "deep_learning_confidence_pct": 21.57,
      "ml_baseline_confidence_pct": 18.79
    }
  ],
  "learning_roadmap": [
    {
      "skill": "Leadership",
      "priority": "High",
      "market_demand_pct": 23.5,
      "stage": "Stage 1: Core Foundation"
    }
  ]
}
```
