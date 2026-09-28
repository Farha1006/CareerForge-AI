"""
CareerForge AI - Phase 5: Machine Learning Evaluation Pipeline
Script: ml/evaluate_ml_model.py
Description: Evaluates the trained ML baseline classifier using Accuracy, Precision,
             Recall, F1-Score, Classification Report, and Confusion Matrix.
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)


def evaluate_pipeline():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    models_dir = os.path.join(script_dir, "models")
    plots_dir = os.path.join(project_root, "data", "processed", "analysis", "plots")

    model_path = os.path.join(models_dir, "career_classifier.joblib")
    le_path = os.path.join(models_dir, "label_encoder.joblib")
    test_data_path = os.path.join(models_dir, "test_data.npz")
    meta_path = os.path.join(models_dir, "model_metadata.json")

    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 5: MODEL EVALUATION", flush=True)
    print("=" * 80, flush=True)

    if not os.path.exists(model_path) or not os.path.exists(test_data_path):
        print("Error: Trained model or test data artifacts missing. Run train_ml_model.py first.")
        sys.exit(1)

    # 1. Load artifacts
    clf = joblib.load(model_path)
    le = joblib.load(le_path)
    test_data = np.load(test_data_path)
    X_test = test_data['X_test']
    y_test = test_data['y_test']

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    print(f"Loaded Model: {meta['model_name']} | Test Samples: {X_test.shape[0]:,}")

    # 2. Predict
    y_pred = clf.predict(X_test)

    # 3. Calculate Overall Metrics
    acc = accuracy_score(y_test, y_pred)
    prec_macro = precision_score(y_test, y_pred, average='macro', zero_division=0)
    rec_macro = recall_score(y_test, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)

    prec_weighted = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec_weighted = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print("\nOVERALL MODEL EVALUATION METRICS:")
    print(f"  - Accuracy:           {acc * 100:.2f}%")
    print(f"  - Weighted Precision: {prec_weighted:.4f}")
    print(f"  - Weighted Recall:    {rec_weighted:.4f}")
    print(f"  - Weighted F1-Score:  {f1_weighted:.4f}")
    print(f"  - Macro Precision:    {prec_macro:.4f}")
    print(f"  - Macro Recall:       {rec_macro:.4f}")
    print(f"  - Macro F1-Score:     {f1_macro:.4f}")

    # 4. Detailed Classification Report
    print("\nDETAILED PER-CLASS CLASSIFICATION REPORT:")
    report_text = classification_report(y_test, y_pred, target_names=le.classes_, zero_division=0)
    print(report_text)

    # 5. Confusion Matrix Visualization
    cm = confusion_matrix(y_test, y_pred)
    classes = list(le.classes_)

    plt.figure(figsize=(10, 8))
    plt.imshow(cm, cmap='Blues', interpolation='nearest')
    plt.colorbar(label='Sample Count')
    plt.xticks(range(len(classes)), classes, rotation=45, ha='right')
    plt.yticks(range(len(classes)), classes)

    # Annotate confusion matrix values
    for i in range(len(classes)):
        for j in range(len(classes)):
            val = cm[i, j]
            if val > 0:
                plt.text(j, i, str(val), ha='center', va='center', color='white' if val > cm.max()/2 else 'black')

    plt.title(f"Confusion Matrix ({meta['model_name']})", fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Career Category', fontsize=12)
    plt.ylabel('True Career Category', fontsize=12)
    plt.tight_layout()

    os.makedirs(plots_dir, exist_ok=True)
    cm_path = os.path.join(plots_dir, "confusion_matrix.png")
    plt.savefig(cm_path, dpi=300)
    plt.close()

    print(f"Saved confusion matrix plot to: {cm_path}")
    print("\n" + "=" * 80, flush=True)
    print("EVALUATION COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    evaluate_pipeline()
