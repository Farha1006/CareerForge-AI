# CareerForge AI - Phase 7: Recommendation Engine & Learning Roadmap Documentation

## Executive Summary

Phase 7 constructs an integrated, multi-layer hybrid recommendation engine and personalized learning roadmap generator for **CareerForge AI**.

It synthesizes empirical Skill-Gap Analysis, Machine Learning baseline predictions (Random Forest Classifier), PyTorch Deep Learning softmax probabilities, and real job market demand stats into a unified recommendation score ($S_{\text{career}} \in [0, 100]$).

---

## 1. Recommendation Logic & Architecture

```
                                +-----------------------------------+
                                |      Student Profile Input        |
                                | (skills, degree, location, target)|
                                +-----------------------------------+
                                                  │
         ┌────────────────────────┬───────────────┴───────────────┬────────────────────────┐
         │                        │                               │                        │
         ▼                        ▼                               ▼                        ▼
+-----------------+   +----------------------+        +-----------------------+  +--------------------+
| Skill-Gap Layer |   | ML Baseline (Phase 5)|        | PyTorch DNN (Phase 6) |  | Market Intel Layer |
| (Skill Match %) |   | (Random Forest Prob) |        | (Softmax Probabilities)|  | (Job Share & Sal)  |
+-----------------+   +----------------------+        +-----------------------+  +--------------------+
         │                        │                               │                        │
         └────────────────────────┴───────────────┬───────────────┴────────────────────────┘
                                                  │
                                                  ▼
                                +-----------------------------------+
                                |      Composite Scoring Engine     |
                                |    S_career Score Calculation     |
                                +-----------------------------------+
                                                  │
                                                  ▼
                                +-----------------------------------+
                                |   Personalized Learning Roadmap   |
                                | (Stage 1 Core -> Stage 3 Mastery) |
                                +-----------------------------------+
```

---

## 2. Composite Scoring Methodology

The recommendation score ($S_{\text{career}}$) for each career category is calculated using a transparent 4-factor formula:

$$S_{\text{career}} = \left( 0.40 \times S_{\text{SkillMatch}} \right) + \left( 0.25 \times P_{\text{DeepLearning}} \right) + \left( 0.20 \times P_{\text{ML Baseline}} \right) + \left( 0.15 \times S_{\text{MarketDemand}} \right)$$

Where:
* **$S_{\text{SkillMatch}}$** (`40%` weight): Case-insensitive match percentage of candidate skills against top required industry skills for that career domain.
* **$P_{\text{DeepLearning}}$** (`25%` weight): PyTorch Deep Neural Network softmax probability percentage for that career category.
* **$P_{\text{ML Baseline}}$** (`20%` weight): Random Forest Classifier prediction probability percentage.
* **$S_{\text{MarketDemand}}$** (`15%` weight): Normalized market hiring volume score ($(\text{MarketShare}_{\text{category}} / \text{MaxMarketShare}) \times 100$).

> **Transparency Policy**: If a student specifies a `target_career`, the engine highlights it but ranks all career categories dynamically based strictly on the composite score without hard-coding preferred outcomes.

---

## 3. Skill-Gap Integration

* The Skill-Gap module ([skill_gap.py](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/ml/skill_gap.py)) performs case-insensitive skill matching against the **15 top skills** per career domain mined during Phase 3.
* Calculates:
  - **Matched Skills**: Skills possessed by student aligned with target role.
  - **Missing Skills**: Industry required skills absent from student profile.
  - **Match Percentage**: $(|\text{Matched}| / |\text{Required}|) \times 100$.

---

## 4. Learning Roadmap Generation Logic

For each identified missing skill, the learning roadmap engine ([learning_roadmap.py](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/ml/learning_roadmap.py)) checks empirical market demand percentages (`demand_pct`) from the database:

1. **Priority Assignment**:
   - **`High Priority`**: Required in $\ge 15.0\%$ of job postings.
   - **`Medium Priority`**: Required in $5.0\% - 15.0\%$ of job postings.
   - **`Standard Priority`**: Required in $< 5.0\%$ of job postings.

2. **Sequential Learning Stages**:
   - **`Stage 1: Core Foundation`**: High market demand skills foundational to multiple roles (e.g. `SQL`, `Python`, `Communication`, `Excel`).
   - **`Stage 2: Technical Specialization`**: Intermediate domain-specific tools (e.g. `AWS`, `ETL`, `Tableau`, `Java`).
   - **`Stage 3: Advanced Mastery`**: Advanced specialized platforms (e.g. `PySpark`, `Docker`, `Kubernetes`, `Databricks`).

---

## 5. Limitations & Future Enhancements

1. **Cold-Start Profiles**: Students entering with 0 listed skills default to broader non-technical market categories (`General Professional / Other`).
2. **Co-Occurrence Weighting**: Future iterations can incorporate association rule confidence weights (from `skill_relationships.csv`) directly into the learning sequence.
