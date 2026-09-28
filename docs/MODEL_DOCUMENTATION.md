# 🤖 Machine Learning & Deep Learning Model Documentation

---

## 1. Overview
CareerForge AI implements a **dual predictive architecture** to predict candidate career domain suitability based on student skill profiles:
1. **Classical ML Baseline Model:** Scikit-Learn **Random Forest Classifier** (`ml/`).
2. **Deep Learning Model:** PyTorch **3-Layer Multi-Layer Perceptron (DNN)** (`deep_learning/`).

Both models are trained on the exact same multi-hot encoded feature representation extracted from **24,444 job listings** in `database/careerforge.db`.

---

## 2. Feature Representation & Preprocessing

### Feature Extraction & Vectorization
- **Raw Input:** List of canonical skill strings associated with each job posting (e.g., `["Python", "SQL", "Pandas", "Scikit-Learn"]`).
- **Feature Encoder:** `MultiLabelBinarizer` (`mlb`) mapping skills into an **87-dimensional binary vector**:
  $$\mathbf{x} = [x_1, x_2, \dots, x_{87}] \in \{0, 1\}^{87}$$
  where $x_i = 1$ if skill $i$ is present, else $0$.

### Target Categories
- **Target Encoder:** `LabelEncoder` mapping job titles into **8 target career classes**:
  0. `Customer Service & Retail`
  1. `Data, AI & Analytics`
  2. `Finance & Accounting`
  3. `General Professional / Other`
  4. `Healthcare & Clinical`
  5. `Management & Operations`
  6. `Sales & Marketing`
  7. `Software & Cloud Engineering`

### Train/Test Split
- **Split Ratio:** 80% Training / 20% Testing (Stratified by target category).
- **Train Samples:** `19,555`
- **Test Samples:** `4,889`

---

## 3. Model 1: Classical ML Baseline (Random Forest)

### Implementation
- **Script:** `ml/train_ml_model.py`
- **Model Artifact:** `ml/models/career_classifier.joblib`
- **Model Metadata:** `ml/models/model_metadata.json`

### Hyperparameters
- **Estimators (`n_estimators`):** `100`
- **Maximum Depth (`max_depth`):** `25`
- **Criterion:** Gini Impurity
- **Jobs (`n_jobs`):** `-1` (Multi-core parallel training)

### Performance Evaluation Metrics
- **Accuracy:** `43.83%`
- **Weighted F1-Score:** `0.3808`

---

## 4. Model 2: PyTorch Deep Neural Network (DNN)

### Implementation
- **Scripts:** `deep_learning/prepare_data.py`, `train_model.py`, `evaluate.py`, `predict.py`
- **Model Checkpoint:** `deep_learning/models/career_dnn_model.pt`
- **Metadata:** `deep_learning/models/dl_metadata.json`

### Network Architecture (`CareerDNN`)

```
Input Vector (87 features)
   │
   ▼
Linear (87 → 128)
   │
   ├──► ReLU Activation
   ├──► BatchNorm1d(128)
   └──► Dropout(p=0.3)
   │
   ▼
Linear (128 → 64)
   │
   ├──► ReLU Activation
   ├──► BatchNorm1d(64)
   └──► Dropout(p=0.2)
   │
   ▼
Linear (64 → 32)
   │
   └──► ReLU Activation
   │
   ▼
Linear (32 → 8 classes)
   │
   └──► Softmax Output Logits
```

### Training Setup & Hyperparameters
- **Loss Function:** `nn.CrossEntropyLoss()`
- **Optimizer:** `torch.optim.Adam(lr=0.001, weight_decay=1e-4)`
- **Batch Size:** `64` (Train) / `128` (Validation)
- **Max Epochs:** `50`
- **Early Stopping:** Patience = 8 (Triggered at Epoch 17)

### Performance Evaluation Metrics
- **Best Validation Loss:** `1.5786`
- **Best Validation Accuracy:** `43.83%` (Epoch 17)
- **Train Loss Convergence:** Reduced from `1.6784` (Epoch 1) to `1.5121` (Epoch 17).

---

## 5. Model Comparison: ML Baseline vs. Deep Learning

| Parameter / Metric | ML Baseline (Random Forest) | PyTorch Deep Neural Network |
| :--- | :--- | :--- |
| **Framework** | Scikit-Learn | PyTorch 2.x |
| **Input Dimensions** | 87 Binary Skill Features | 87 Binary Skill Tensors |
| **Output Layer** | Decision Tree Voting Ensembles | 8-Class Logits + Softmax Probabilities |
| **Training Samples** | 19,555 | 19,555 |
| **Test Accuracy** | **43.83%** | **43.83%** |
| **Inference Output** | Class probabilities | Normalized Softmax Probability Distribution |
| **Execution Time** | ~15ms / batch | ~8ms / batch |
| **Model Size** | ~14.2 MB (`.joblib`) | ~112 KB (`.pt`) |

---

## 6. Model Serving in Recommendation Engine

When a student submits their skills:
1. `ml/predict_career.py` vectorizes skills and executes `rf_clf.predict_proba(X)`.
2. `deep_learning/predict.py` passes skills through `CareerDNN` and evaluates `torch.softmax(logits)`.
3. Both prediction vectors are passed to `CareerRecommendationEngine` to compute composite recommendation scores.
