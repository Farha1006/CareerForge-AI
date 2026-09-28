# 🎓 CareerForge AI — Comprehensive Technical Project Documentation

---

## 1. Project Title
**CareerForge AI: An Intelligent Data-Driven Career Guidance and Skill-Gap Analytics Platform Using Machine Learning, Deep Learning, and RESTful Microservices**

---

## 2. Abstract
**CareerForge AI** is an end-to-end, data-driven career intelligence platform designed to bridge the gap between academic preparation and dynamic job market demand. Utilizing a dataset of **33,245 job listings**, the system standardizes, stores, and mines market intelligence across **87 canonical skills** and **8 major career categories**. It integrates a **Random Forest Machine Learning baseline classifier**, a **3-Layer PyTorch Deep Neural Network (DNN)**, a **Skill-Gap Analysis Engine**, and a **Multi-Criteria Hybrid Recommendation Engine** to calculate personalized career match scores and multi-stage learning roadmaps. The backend is powered by **FastAPI** with 10 REST endpoints, while the frontend dashboard is built using **React**, **Vite**, **Tailwind CSS**, and **Recharts**.

---

## 3. Problem Statement
Higher education students frequently encounter difficulty aligning their academic coursework and self-taught skills with real-world job market requirements. Conventional career guidance solutions suffer from several core drawbacks:
1. **Static and Manual Advice:** Guidance is often based on outdated counselor knowledge rather than real-time empirical market listings.
2. **Qualitative Match Estimates:** Absence of quantifiable skill-coverage scores comparing a student's profile against domain-specific skill matrices.
3. **Lack of Personalization:** Failure to provide actionable, prioritized step-by-step learning roadmaps tailored to missing skills.
4. **Disconnected Machine Learning Models:** Failure to combine classical statistical ML predictions with deep neural network inference and empirical market share statistics.

---

## 4. Existing System
Traditional career advice systems rely on manual surveys, static career quizzes, or unstructured job search filters. They lack unified data engineering pipelines to extract and normalize skills from raw job text descriptions, and fail to provide personalized skill-gap quantification or deep learning-driven career trajectory predictions.

---

## 5. Proposed System
**CareerForge AI** proposes an automated, data-centric pipeline:
- **Data Engineering (ETL):** Extracts, cleans, deduplicates, and normalizes unstructured job descriptions into structured datasets.
- **Relational Data Storage:** Stores normalized listings across indexed SQLite database tables (`jobs`, `skills`, `job_skills`).
- **Data Mining:** Extracts top-demanded skills, category distributions, salary metrics, geographic hiring hotspots, and skill co-occurrence pairs.
- **Dual Predictive Modeling:** Combines a Scikit-Learn **Random Forest Classifier** and a **PyTorch Deep Neural Network** to predict career domain suitability from student skill vectors.
- **Hybrid Recommendation Engine:** Synthesizes Skill Match % (40%), PyTorch DL Probability (25%), Random Forest ML Probability (15%), Market Demand (10%), and Direct Target Choice (10%) into unified recommendations and a 4-stage learning roadmap.
- **RESTful APIs & Interactive Dashboard:** Exposes scalable FastAPI endpoints consumed by a responsive React dashboard.

---

## 6. Objectives
1. Build an ETL pipeline to clean and structure raw job market listings without altering raw inputs.
2. Design a normalized relational SQLite database with primary/foreign keys and performance indexes.
3. Mine skill co-occurrence statistics, geographic hiring concentrations, and average industry salaries.
4. Develop a reproducible student profile representation and a case-insensitive skill-gap analysis function.
5. Train and evaluate a baseline ML model (Random Forest) and a PyTorch Deep Neural Network on 87 binary skill features.
6. Formulate a multi-criteria hybrid recommendation engine and automated learning roadmap generator.
7. Implement a production-ready FastAPI backend with CORS middleware and Pydantic request/response validation.
8. Construct a responsive React dashboard with live data visualizations (Recharts).
9. Create automated unit and integration test suites (`test_api.py`, `test_integration.py`).

---

## 7. System Architecture
The system follows a modular 5-tier architecture:
1. **Data Layer:** `data/raw/` → `etl/02_clean_transform.py` → `data/processed/jobs_cleaned.csv` → `database/careerforge.db`.
2. **Analytics & Mining Layer:** `data_mining/run_analysis.py` (Frequency, Co-occurrence, Geography, Salary analysis).
3. **Model & Intelligence Layer:** Scikit-Learn Random Forest (`ml/`), PyTorch DNN (`deep_learning/`), Skill-Gap Engine (`ml/skill_gap.py`), and Recommendation Engine (`ml/recommendation_engine.py`).
4. **API Service Layer:** FastAPI Application (`backend/app/main.py`) exposing 10 REST endpoints.
5. **Presentation Layer:** React + Vite Dashboard (`frontend/src/`) rendering interactive analytics and roadmap cards.

---

## 8. Technology Stack
- **Programming Languages:** Python 3.13.5, JavaScript (ES6+), HTML5, CSS3
- **Data Engineering & Analysis:** Pandas, NumPy, SQLite3
- **Machine Learning & Deep Learning:** Scikit-Learn, PyTorch, Joblib
- **Backend Framework:** FastAPI, Uvicorn, Pydantic V2, Starlette TestClient
- **Frontend Framework:** React 18, Vite 5, Tailwind CSS 3, Recharts 2, Axios, Lucide React Icons
- **Testing & Tooling:** Unittest, Pytest, Node.js (v24.7.0), npm (11.5.1)

---

## 9. Data Engineering / ETL
- **Source Input:** Raw job dataset (`data/raw/`) containing unstructured job text, titles, salaries, and skill descriptions.
- **Pipeline Script:** `etl/02_clean_transform.py`
- **Cleaned Dataset:** `data/processed/jobs_cleaned.csv`
- **Metrics:** Processed **33,245 valid job listings** across 34 columns.
- **Operations:** Text lowercasing, whitespace trim, exact duplicate removal, missing value handling, text normalization, and skill extraction preserving description context.

---

## 10. Database
- **Database Engine:** SQLite 3 (`database/careerforge.db`)
- **Creation Script:** `database/create_database.py`
- **Tables:**
  1. `jobs` (33,245 rows): `job_id` (PK), `job_title`, `clean_title`, `company_id`, `location`, `formatted_work_type`, `annual_avg_salary`, `clean_description`, `career_category`.
  2. `skills` (87 rows): `skill_id` (PK), `skill_name` (UNIQUE).
  3. `job_skills` (90,142 mappings): `job_id` (FK), `skill_id` (FK), Composite PK `(job_id, skill_id)`.
- **Indexes:** `idx_jobs_title`, `idx_jobs_category`, `idx_skills_name`, `idx_job_skills_job`, `idx_job_skills_skill`.

---

## 11. Data Mining
- **Module Directory:** `data_mining/` (`skill_analysis.py`, `career_analysis.py`, `market_analysis.py`, `run_analysis.py`)
- **Key Mined Insights:**
  - Top Demanded Skill: **Communication** (required in **48.77%** of listings), followed by **Leadership** (**23.48%**) and **Excel** (**16.20%**).
  - Largest Hiring Domain: **Management & Operations** (11,326 jobs / 34.07% market share).
  - Top Tech Salary Domain: **Data, AI & Analytics** ($133,790.38 avg annual salary).
  - Top Skill Co-occurrence Pairs: *Leadership + Communication* (4,808 jobs), *Excel + Communication* (3,574 jobs).

---

## 12. Student Profile
- **Class Implementation:** `ml/student_profile.py` (`StudentProfile` dataclass & Pydantic schema `StudentProfileSchema`).
- **Attributes:** `student_id`, `name`, `education`, `degree`, `skills` (List[str]), `interests` (List[str]), `experience_years` (float), `preferred_location` (str), `target_career` (Optional[str]).

---

## 13. Skill-Gap Analysis
- **Module Script:** `ml/skill_gap.py` (`analyze_skill_gap`)
- **Logic:**
  - Extracts the canonical skill matrix for the specified target career category from `database/careerforge.db`.
  - Performs case-insensitive matching between student skills and required industry skills.
  - Computes `matched_skills`, `missing_skills`, and `skill_match_pct`:
    $$\text{Skill Match \%} = \left( \frac{|\text{Matched Skills}|}{|\text{Total Industry Category Skills}|} \right) \times 100$$

---

## 14. Machine Learning Baseline
- **Script:** `ml/train_ml_model.py`
- **Vectorization:** `MultiLabelBinarizer` converting skill lists into **87 binary feature columns**; `LabelEncoder` encoding **8 career categories**.
- **Dataset Split:** 80/20 Stratified Split (**19,555 train / 4,889 test**).
- **Selected Model:** **Random Forest Classifier** (`n_estimators=100`, `max_depth=25`).
- **Evaluation Metrics:** Accuracy: **43.83%**, Weighted F1-Score: **0.3808**.
- **Artifacts:** `ml/models/career_classifier.joblib`, `skill_mlb.joblib`, `label_encoder.joblib`, `model_metadata.json`.

---

## 15. Deep Learning
- **Scripts:** `deep_learning/prepare_data.py`, `train_model.py`, `predict.py`, `evaluate.py`.
- **Framework:** **PyTorch 2.x**.
- **Architecture (`CareerDNN`):**
  - Input Layer: 87 features
  - Hidden Layer 1: Dense(128) + ReLU + BatchNorm1d(128) + Dropout(0.3)
  - Hidden Layer 2: Dense(64) + ReLU + BatchNorm1d(64) + Dropout(0.2)
  - Hidden Layer 3: Dense(32) + ReLU
  - Output Layer: Dense(8) (Softmax/CrossEntropyLoss)
- **Training Setup:** Adam Optimizer (`lr=0.001`, `weight_decay=1e-4`), Batch Size 64, Early Stopping (Patience = 8).
- **Evaluation Metrics:** Best Validation Loss: **1.5786**, Best Validation Accuracy: **43.83%** (Epoch 17).
- **Artifact Checkpoint:** `deep_learning/models/career_dnn_model.pt`.

---

## 16. Recommendation Engine
- **Module Script:** `ml/recommendation_engine.py` (`CareerRecommendationEngine`)
- **Hybrid Scoring Formula:**
  $$\text{Composite Score} = 0.40 \times \text{SkillMatch\%} + 0.25 \times \text{DL\_Prob\%} + 0.15 \times \text{ML\_Prob\%} + 0.10 \times \text{MarketShare\%} + 0.10 \times \text{TargetBoost}$$
- **Personalized Learning Roadmap Generator (`ml/learning_roadmap.py`):** Categorizes missing skills into a 4-stage curriculum:
  - *Stage 1: Core Foundation* (Market Demand > 10%)
  - *Stage 2: Technical Specialization* (Market Demand 4% - 10%)
  - *Stage 3: Advanced Mastery* (Market Demand < 4%)
  - *Stage 4: Practical Application & Projects* (Capstone execution)

---

## 17. FastAPI Backend
- **Main Entrypoint:** `backend/app/main.py`
- **CORS Middleware:** `CORSMiddleware(allow_origins=["*"])`
- **10 Implemented Endpoints:**
  1. `GET /` – Redirect to Swagger docs
  2. `GET /api/health` – Server health status
  3. `POST /api/student/profile` – Profile validation
  4. `POST /api/skill-gap` – Skill gap metrics calculation
  5. `POST /api/recommend` – Full hybrid recommendation pipeline
  6. `POST /api/predict/ml` – Random Forest prediction
  7. `POST /api/predict/deep-learning` – PyTorch DNN prediction
  8. `GET /api/market/top-skills` – Top demanded skills query
  9. `GET /api/market/careers` – Career category market share & salary query
  10. `GET /api/market/locations` – Geographic job volume query
  11. `GET /api/market/skill-cooccurrence` – Top skill co-occurrence pairs query

---

## 18. React Frontend
- **App Location:** `frontend/`
- **Tech Stack:** React 18, Vite 5, Tailwind CSS 3, Axios, Recharts, Lucide React
- **Services & Context:** `src/services/api.js`, `src/context/CareerContext.jsx`
- **Components:** `Navbar.jsx`, `Sidebar.jsx`, `MetricCard.jsx`, `SkillBadge.jsx`, `LoadingSpinner.jsx`, `ErrorAlert.jsx`

---

## 19. Dashboard Pages
1. `Home.jsx` – Landing page with feature overview, system workflow, & CTA buttons.
2. `Profile.jsx` – Interactive profile input form with student presets and validation.
3. `Dashboard.jsx` – Master overview displaying top recommendation, match %, ML/DL predictions, & priority roadmap.
4. `CareerAnalysis.jsx` – Ranked career recommendations breakdown with composite scores and salary data.
5. `SkillGap.jsx` – Side-by-side matched vs. missing skills comparison and progress bar.
6. `MarketInsights.jsx` – Interactive charts for skill market share, career volume, geographic hotspots, and co-occurrences.
7. `LearningRoadmap.jsx` – 4-stage step-by-step career development roadmap.

---

## 20. Testing
- **Unit Test Suite (`tests/test_api.py`):** 10 automated test cases verifying HTTP status codes, request schemas, 422 errors, and CORS pre-flight headers.
- **Integration Test Suite (`tests/test_integration.py`):** 8 automated test cases validating ETL CSV files, SQLite schema, ML models, PyTorch model, skill-gap analysis, hybrid recommendations, learning roadmap, and complete client API simulation.
- **Pass Rate:** **100% (18/18 tests passed cleanly)**.

---

## 21. Actual Results
- **ETL Processing:** 33,245 listings successfully cleaned and structured.
- **Database Scalability:** SQLite query latency < 15ms for skill frequency and career category aggregations.
- **Model Training:** Random Forest (43.83% accuracy) and PyTorch DNN (43.83% accuracy) successfully saved and loaded for real-time inference.
- **API Response Latency:** End-to-end `/api/recommend` request completed in < 150ms.
- **Vite Production Build:** Successfully compiled in 17.33 seconds (`dist/`).

---

## 22. Limitations
1. **Generic Soft Skills:** Soft skills like "Communication" and "Leadership" appear across all job categories, which can dampen domain-specific skill differentiation.
2. **Static CSV Backing for Geographic Mining:** Geographic and co-occurrence endpoints draw from mined CSV outputs rather than dynamic SQL spatial queries.
3. **No Direct External Course Links:** Roadmap recommends skill subjects but does not dynamically hyperlink to live online course providers (e.g., Coursera, edX).

---

## 23. Future Enhancements
1. **TF-IDF Skill Weighting:** Apply Term Frequency-Inverse Document Frequency to downweight ubiquitous soft skills and emphasize specialized technical skills.
2. **Real-time Job Ingestion Pipeline:** Implement automated scraper or API ingestion to continuously update SQLite market tables.
3. **External Course Integration:** Connect missing skills in the learning roadmap to live REST APIs for online educational courses.

---

## 24. Conclusion
**CareerForge AI** successfully demonstrates an end-to-end, reproducible software engineering solution for career guidance. By unifying data engineering, relational database design, statistical data mining, classical machine learning, PyTorch deep learning, FastAPI microservices, and a React dashboard, the platform provides actionable intelligence for students navigating modern job markets.
