# CareerForge AI - Phase 5: Machine Learning Career Prediction Baseline Report

## Executive Summary

Phase 5 implements a supervised machine-learning baseline model designed to predict a candidate's target career category from their skill profile. The pipeline trains on **24,444 job postings** extracted from `database/careerforge.db` and evaluates multi-class classification performance across **8 distinct career domains**.

---

## 1. Feature Representation & Input Vectorization

* **Input Features**: Binary / Multi-Hot Skill Vectors generated using `MultiLabelBinarizer` across **87 canonical skills**.
* **Vector Dimension**: Sparse binary vector $X \in \{0, 1\}^{N \times 87}$, where $X_{i, j} = 1$ if skill $j$ is present in posting $i$, else $0$.
* **Leakage Control**: Target career choices or user preferences are **strictly excluded** from input features to prevent data leakage. The model learns exclusively from raw skill associations.

---

## 2. Target Variable & Category Classes

The target variable ($y$) represents the career domain mapped from job titles into **8 mutually exclusive classes**:

1. **`Customer Service & Retail`**
2. **`Data, AI & Analytics`**
3. **`Finance & Accounting`**
4. **`General Professional / Other`**
5. **`Healthcare & Clinical`**
6. **`Management & Operations`**
7. **`Sales & Marketing`**
8. **`Software & Cloud Engineering`**

---

## 3. Data Preprocessing & Split Strategy

* **Total Samples**: **24,444** job postings with extracted skill vectors.
* **Train / Test Split**: **80% Training (`19,555` samples) / 20% Testing (`4,889` samples)** using Stratified Random Sampling (`stratify=y`, `random_state=42`).
* **Class Weighting**: Balanced class weights applied to penalize majority-class bias.

---

## 4. Model Selection & Candidate Benchmarks

Two primary baseline algorithms were trained and evaluated on identical test splits:

| Model Classifier | Hyperparameters | Accuracy | Weighted F1-Score | Status |
| :--- | :--- | :---: | :---: | :---: |
| **Random Forest Classifier** | `n_estimators=100`, `max_depth=25`, `random_state=42` | **43.83%** | **0.3808** | **Selected Best Baseline** |
| **Logistic Regression** | `max_iter=1000`, `class_weight='balanced'` | **27.16%** | **0.2415** | Candidate |

---

## 5. Model Evaluation Metrics

### Overall Metrics (Random Forest Classifier)

* **Accuracy**: **43.83%**
* **Weighted Precision**: **0.4397**
* **Weighted Recall**: **0.4383**
* **Weighted F1-Score**: **0.3808**
* **Macro Precision**: **0.3993**
* **Macro Recall**: **0.2731**
* **Macro F1-Score**: **0.2660**

---

### Detailed Per-Class Evaluation Metrics

| Career Category | Precision | Recall | F1-Score | Support (Test Samples) |
| :--- | :---: | :---: | :---: | :---: |
| **Software & Cloud Engineering** | **0.68** | **0.45** | **0.54** | 853 |
| **Data, AI & Analytics** | **0.67** | **0.39** | **0.49** | 189 |
| **General Professional / Other** | **0.40** | **0.68** | **0.50** | 1,507 |
| **Management & Operations** | **0.41** | **0.61** | **0.49** | 1,053 |
| **Sales & Marketing** | **0.54** | **0.03** | **0.05** | 545 |
| **Finance & Accounting** | **0.31** | **0.02** | **0.04** | 175 |
| **Healthcare & Clinical** | **0.20** | **0.01** | **0.01** | 373 |
| **Customer Service & Retail** | **0.00** | **0.00** | **0.00** | 194 |

---

## 6. Confusion Matrix & Artifact Locations

* **Trained Classifier**: [career_classifier.joblib](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/ml/models/career_classifier.joblib)
* **Skill Transformer**: [skill_mlb.joblib](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/ml/models/skill_mlb.joblib)
* **Label Encoder**: [label_encoder.joblib](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/ml/models/label_encoder.joblib)
* **Confusion Matrix Visualization**: [confusion_matrix.png](file:///c:/Users/sheer/OneDrive/Documents/CareerForge-AI/data/processed/analysis/plots/confusion_matrix.png)

---

## 7. Model Limitations & Observations

1. **Skill Overlap Across Domains**: High-frequency skills like `Communication` and `Leadership` appear across non-technical job postings, causing generic skill sets to predict into `General Professional / Other` or `Management & Operations`.
2. **High Precision for Technical Roles**: Specialized technical skills (`AWS`, `Docker`, `Kubernetes`, `PySpark`) achieve high precision (**68%** for Software Engineering, **67%** for Data/AI).
3. **Future Deep Learning Upgrade**: Phase 6 will implement Deep NLP embeddings (Sentence Transformers / BERT) on unstructured `job_description` text to capture nuanced context beyond discrete binary skill vectors.
