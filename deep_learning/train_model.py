"""
CareerForge AI - Phase 6: Deep Learning Model Training Module
Script: deep_learning/train_model.py
Description: Trains a Multi-Layer Feed-Forward Neural Network (DNN) using PyTorch,
             featuring BatchNorm, Dropout, Early Stopping, and Adam optimization.
             Saves trained model weights to deep_learning/models/career_dnn_model.pt.
"""

import os
import sys
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from sklearn.model_selection import train_test_split


def get_paths():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(script_dir, "models")
    data_path = os.path.join(models_dir, "prepared_dl_data.npz")
    model_path = os.path.join(models_dir, "career_dnn_model.pt")
    meta_path = os.path.join(models_dir, "dl_metadata.json")
    return models_dir, data_path, model_path, meta_path


# Define Neural Network Architecture
class CareerDNN(nn.Module):
    """
    Feed-Forward Neural Network for Multi-Class Career Prediction.
    Architecture:
      Input (87) -> Dense(128) -> ReLU -> BatchNorm -> Dropout(0.3)
                 -> Dense(64)  -> ReLU -> BatchNorm -> Dropout(0.2)
                 -> Dense(32)  -> ReLU
                 -> Output(num_classes)
    """

    def __init__(self, input_dim: int, num_classes: int):
        super(CareerDNN, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.3),

            nn.Linear(128, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.2),

            nn.Linear(64, 32),
            nn.ReLU(),

            nn.Linear(32, num_classes)
        )

    def forward(self, x):
        return self.network(x)


def train_dnn():
    models_dir, data_path, model_path, meta_path = get_paths()

    print("=" * 80, flush=True)
    print("CAREERFORGE AI - PHASE 6: DEEP LEARNING MODEL TRAINING", flush=True)
    print("=" * 80, flush=True)

    if not os.path.exists(data_path):
        print("Error: Prepared dataset missing. Run deep_learning/prepare_data.py first.")
        sys.exit(1)

    # 1. Load Data
    data = np.load(data_path)
    X_train_full = data['X_train']
    y_train_full = data['y_train']
    X_test_arr = data['X_test']
    y_test_arr = data['y_test']

    # 2. Validation Split (80% Train, 20% Val)
    X_train_arr, X_val_arr, y_train_arr, y_val_arr = train_test_split(
        X_train_full, y_train_full, test_size=0.20, random_state=42, stratify=y_train_full
    )

    print(f"Data Split for Training:")
    print(f"  - Train Set:      {X_train_arr.shape[0]:,} samples")
    print(f"  - Validation Set: {X_val_arr.shape[0]:,} samples")
    print(f"  - Test Set:       {X_test_arr.shape[0]:,} samples")

    input_dim = X_train_arr.shape[1]
    num_classes = len(np.unique(y_train_full))

    # Convert to PyTorch Tensors
    X_train_t = torch.tensor(X_train_arr, dtype=torch.float32)
    y_train_t = torch.tensor(y_train_arr, dtype=torch.long)

    X_val_t = torch.tensor(X_val_arr, dtype=torch.float32)
    y_val_t = torch.tensor(y_val_arr, dtype=torch.long)

    train_dataset = TensorDataset(X_train_t, y_train_t)
    val_dataset = TensorDataset(X_val_t, y_val_t)

    train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=128, shuffle=False)

    # 3. Model Initialization
    model = CareerDNN(input_dim=input_dim, num_classes=num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)

    print(f"\nNeural Network Architecture Initialized:")
    print(f"  - Input Layer:  {input_dim} features")
    print(f"  - Hidden Layers: 128 (ReLU + BN + Dropout) -> 64 (ReLU + BN + Dropout) -> 32 (ReLU)")
    print(f"  - Output Layer: {num_classes} classes (Softmax/Logits)")
    print(f"  - Loss Function: CrossEntropyLoss | Optimizer: Adam (lr=0.001)")

    # 4. Training Loop with Early Stopping
    max_epochs = 50
    patience = 8
    best_val_loss = float('inf')
    patience_counter = 0
    best_model_state = None

    history = {"train_loss": [], "val_loss": [], "val_acc": []}

    print("\nStarting Deep Learning Training Loop:", flush=True)

    for epoch in range(1, max_epochs + 1):
        model.train()
        running_train_loss = 0.0

        for batch_x, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            running_train_loss += loss.item() * batch_x.size(0)

        epoch_train_loss = running_train_loss / len(train_dataset)

        # Validation evaluation
        model.eval()
        running_val_loss = 0.0
        val_correct = 0

        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                outputs = model(batch_x)
                loss = criterion(outputs, batch_y)
                running_val_loss += loss.item() * batch_x.size(0)
                preds = torch.argmax(outputs, dim=1)
                val_correct += (preds == batch_y).sum().item()

        epoch_val_loss = running_val_loss / len(val_dataset)
        epoch_val_acc = (val_correct / len(val_dataset)) * 100.0

        history["train_loss"].append(round(epoch_train_loss, 4))
        history["val_loss"].append(round(epoch_val_loss, 4))
        history["val_acc"].append(round(epoch_val_acc, 2))

        if epoch % 5 == 0 or epoch == 1:
            print(f"  Epoch [{epoch:02d}/{max_epochs:02d}] -> Train Loss: {epoch_train_loss:.4f} | Val Loss: {epoch_val_loss:.4f} | Val Acc: {epoch_val_acc:.2f}%", flush=True)

        # Early Stopping check
        if epoch_val_loss < best_val_loss:
            best_val_loss = epoch_val_loss
            patience_counter = 0
            best_model_state = model.state_dict().copy()
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"\n  [Early Stopping Triggered at Epoch {epoch}] Best Val Loss: {best_val_loss:.4f}", flush=True)
                break

    # Restore best model state and save
    if best_model_state is not None:
        model.load_state_dict(best_model_state)

    torch.save(model.state_dict(), model_path)

    metadata = {
        "architecture": "3-Layer Feed-Forward Neural Network (DNN)",
        "input_dim": input_dim,
        "num_classes": num_classes,
        "best_val_loss": round(best_val_loss, 4),
        "total_epochs_trained": len(history["train_loss"]),
        "history": history
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nSaved PyTorch DNN model checkpoint to: {model_path}")
    print(f"Saved training metadata to: {meta_path}")

    print("\n" + "=" * 80, flush=True)
    print("DEEP LEARNING MODEL TRAINING COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    train_dnn()
