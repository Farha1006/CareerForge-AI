# CareerForge AI - Deep Learning Module

## Overview

The `deep_learning/` module implements a PyTorch-based Multi-Layer Feed-Forward Neural Network (DNN) for multi-class career category classification.

It receives multi-hot binary skill vectors ($X \in \{0, 1\}^{N \times 87}$) matching the Phase 5 ML pipeline vocabulary, passing them through a 3-hidden-layer deep network with Batch Normalization, Dropout regularization, and Softmax activation.

---

## Neural Network Architecture

```
                       Input Layer (87 Binary Skill Features)
                                         │
                                         ▼
                      Dense Layer 1: Linear(87 -> 128)
                                         │
                                   ReLU Activation
                                         │
                              Batch Normalization (128)
                                         │
                                Dropout (Rate = 0.3)
                                         │
                                         ▼
                      Dense Layer 2: Linear(128 -> 64)
                                         │
                                   ReLU Activation
                                         │
                               Batch Normalization (64)
                                         │
                                Dropout (Rate = 0.2)
                                         │
                                         ▼
                      Dense Layer 3: Linear(64 -> 32)
                                         │
                                   ReLU Activation
                                         │
                                         ▼
                     Output Layer: Linear(32 -> 8 Classes)
                                         │
                             Softmax Probability Logits
```

---

## Files & Modules

* **`prepare_data.py`**: Extracts job skills and maps target categories from `database/careerforge.db`, outputting PyTorch-ready dataset tensors (`prepared_dl_data.npz`).
* **`train_model.py`**: Builds the `CareerDNN` PyTorch model, executes 80/20 train-validation training with early stopping (patience=8), and exports model weights (`career_dnn_model.pt`).
* **`evaluate.py`**: Evaluates model performance on the holdout test set (`4,889` samples), calculating Accuracy, Precision, Recall, F1-Score, and saving confusion matrix (`dl_confusion_matrix.png`).
* **`predict.py`**: Inference engine (`DeepLearningCareerPredictor`) taking a candidate's skill list and returning top predicted categories with confidence percentages.
* **`DL_REPORT.md`**: Comprehensive deep learning report comparing DNN performance against the Phase 5 Random Forest ML baseline.

---

## Execution Instructions

1. **Prepare Tensors**:
   ```bash
   python deep_learning/prepare_data.py
   ```
2. **Train Deep Neural Network**:
   ```bash
   python deep_learning/train_model.py
   ```
3. **Evaluate Test Metrics & Confusion Matrix**:
   ```bash
   python deep_learning/evaluate.py
   ```
4. **Test Prediction Inference**:
   ```bash
   python deep_learning/predict.py
   ```
