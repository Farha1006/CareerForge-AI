"""
CareerForge AI - Phase 6: Deep Learning Model Evaluation Pipeline
Script: deep_learning/evaluate.py
Description: Evaluates the trained PyTorch Deep Learning model on test set samples,
             computing Accuracy, Precision, Recall, F1-Score, and saving confusion matrix plot.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from train_model import CareerDNN


def evaluate_dl_model():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    models_dir = os.path.join(script_dir, "models")
    plots_dir = os.path.join(project_root, "data", "processed", "analysis", "plots")

    model_path = os.path.join(models_dir, "career_dnn_model.pt")
    le_path = os.path.join(models_dir, "dl_label_encoder.joblib")
    data_path = os.path.join(models_dir, "prepared_dl_data.npz")
    meta_path = os.path.join(models_dir, "dl_metadata.json")

    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 6: DEEP LEARNING MODEL EVALUATION", flush=True)
    print("=" * 80, flush=True)

    if not os.path.exists(model_path) or not os.path.exists(data_path):
        print("Error: Trained model or dataset artifacts missing. Run prepare_data.py and train_model.py first.")
        sys.exit(1)

    # 1. Load Artifacts
    data = np.load(data_path)
    X_test_arr = data['X_test']
    y_test_arr = data['y_test']

    le = joblib.load(le_path)
    classes = list(le.classes_)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # 2. Instantiate and Load Model
    input_dim = X_test_arr.shape[1]
    num_classes = len(classes)
    model = CareerDNN(input_dim=input_dim, num_classes=num_classes)
    model.load_state_dict(torch.load(model_path))
    model.eval()

    # 3. Perform Forward Pass Evaluation
    X_test_t = torch.tensor(X_test_arr, dtype=torch.float32)
    with torch.no_grad():
        logits = model(X_test_t)
        probs = torch.softmax(logits, dim=1).numpy()
        y_pred = np.argmax(probs, axis=1)

    # 4. Compute Metrics
    acc = accuracy_score(y_test_arr, y_pred)
    prec_macro = precision_score(y_test_arr, y_pred, average='macro', zero_division=0)
    rec_macro = recall_score(y_test_arr, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test_arr, y_pred, average='macro', zero_division=0)

    prec_weighted = precision_score(y_test_arr, y_pred, average='weighted', zero_division=0)
    rec_weighted = recall_score(y_test_arr, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test_arr, y_pred, average='weighted', zero_division=0)

    print(f"Loaded PyTorch DNN Checkpoint | Test Set: {X_test_arr.shape[0]:,} samples")

    print("\nDEEP LEARNING MODEL EVALUATION METRICS:")
    print(f"  - Accuracy:           {acc * 100:.2f}%")
    print(f"  - Weighted Precision: {prec_weighted:.4f}")
    print(f"  - Weighted Recall:    {rec_weighted:.4f}")
    print(f"  - Weighted F1-Score:  {f1_weighted:.4f}")
    print(f"  - Macro Precision:    {prec_macro:.4f}")
    print(f"  - Macro Recall:       {rec_macro:.4f}")
    print(f"  - Macro F1-Score:     {f1_macro:.4f}")

    print("\nDETAILED PER-CLASS CLASSIFICATION REPORT:")
    report_text = classification_report(y_test_arr, y_pred, target_names=classes, zero_division=0)
    print(report_text)

    # 5. Save Confusion Matrix Plot
    cm = confusion_matrix(y_test_arr, y_pred)

    plt.figure(figsize=(10, 8))
    plt.imshow(cm, cmap='Purples', interpolation='nearest')
    plt.colorbar(label='Sample Count')
    plt.xticks(range(len(classes)), classes, rotation=45, ha='right')
    plt.yticks(range(len(classes)), classes)

    for i in range(len(classes)):
        for j in range(len(classes)):
            val = cm[i, j]
            if val > 0:
                plt.text(j, i, str(val), ha='center', va='center', color='white' if val > cm.max()/2 else 'black')

    plt.title("Confusion Matrix (PyTorch Deep Neural Network)", fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Career Category', fontsize=12)
    plt.ylabel('True Career Category', fontsize=12)
    plt.tight_layout()

    os.makedirs(plots_dir, exist_ok=True)
    cm_path = os.path.join(plots_dir, "dl_confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()

    print(f"Saved Deep Learning confusion matrix plot to: {cm_path}")
    print("\n" + "=" * 80, flush=True)
    print("DEEP LEARNING EVALUATION COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    evaluate_dl_model()
