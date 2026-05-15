#!/usr/bin/env python3
"""
Skin Lesion Classification Model Evaluation Script

Loads trained ResNet18 model and evaluates on test dataset.
Computes accuracy, precision, recall, F1, confusion matrix, and per-class metrics.
"""

import os
import argparse
import numpy as np
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    label_binarize
)
import matplotlib.pyplot as plt
import seaborn as sns


# ========== CONFIGURATION ==========

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = "skin_ai_demo/model/best_skin_model.pt"
CLASS_NAMES = ["nevus", "melanoma", "bcc", "other"]
NUM_CLASSES = 4
IMAGE_SIZE = 224
BATCH_SIZE = 32


# ========== MODEL RECONSTRUCTION ==========

def build_model():
    """Reconstruct exact ResNet18 architecture from training"""
    from torchvision.models import resnet18
    
    model = resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model


def load_checkpoint(model, checkpoint_path):
    """Load trained weights into model"""
    if not os.path.exists(checkpoint_path):
        raise FileNotFoundError(f"Model checkpoint not found: {checkpoint_path}")
    
    state_dict = torch.load(checkpoint_path, map_location=DEVICE)
    model.load_state_dict(state_dict)
    print(f"✓ Model loaded from {checkpoint_path}")
    return model


# ========== PREPROCESSING ==========

def get_transforms():
    """Apply same transforms used during training/inference"""
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        # Note: Add ImageNet normalization if used during training
        # transforms.Normalize(
        #     mean=[0.485, 0.456, 0.406],
        #     std=[0.229, 0.224, 0.225]
        # )
    ])


# ========== EVALUATION ==========

def evaluate_model(model, data_loader):
    """Run model evaluation on test set"""
    model.eval()
    
    all_preds = []
    all_labels = []
    all_probs = []
    
    with torch.no_grad():
        for images, labels in data_loader:
            images = images.to(DEVICE)
            labels = labels.to(DEVICE)
            
            outputs = model(images)
            probs = torch.nn.functional.softmax(outputs, dim=1)
            preds = outputs.argmax(dim=1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    return np.array(all_preds), np.array(all_labels), np.array(all_probs)


def print_metrics(y_true, y_pred, y_probs):
    """Print comprehensive evaluation metrics"""
    
    accuracy = accuracy_score(y_true, y_pred)
    precision_macro = precision_score(y_true, y_pred, average='macro', zero_division=0)
    recall_macro = recall_score(y_true, y_pred, average='macro', zero_division=0)
    f1_macro = f1_score(y_true, y_pred, average='macro', zero_division=0)
    
    print("\n" + "="*60)
    print("MODEL EVALUATION RESULTS")
    print("="*60)
    
    print(f"\n{'Metric':<25} {'Value':>10}")
    print("-" * 60)
    print(f"{'Accuracy':<25} {accuracy:>10.4f}")
    print(f"{'Precision (macro)':<25} {precision_macro:>10.4f}")
    print(f"{'Recall (macro)':<25} {recall_macro:>10.4f}")
    print(f"{'F1-Score (macro)':<25} {f1_macro:>10.4f}")
    
    # Per-class metrics
    print("\n" + "-"*60)
    print("PER-CLASS METRICS:")
    print("-"*60)
    
    for i, class_name in enumerate(CLASS_NAMES):
        class_mask = y_true == i
        if class_mask.sum() > 0:
            class_acc = (y_pred[class_mask] == i).mean()
            class_prec = precision_score(y_true, y_pred, labels=[i], average='macro', zero_division=0)
            class_rec = recall_score(y_true, y_pred, labels=[i], average='macro', zero_division=0)
            print(f"\n{class_name.upper()}")
            print(f"  Samples: {class_mask.sum()}")
            print(f"  Accuracy: {class_acc:.4f}")
            print(f"  Precision: {class_prec:.4f}")
            print(f"  Recall: {class_rec:.4f}")
    
    # Full classification report
    print("\n" + "="*60)
    print("DETAILED CLASSIFICATION REPORT:")
    print("="*60)
    print(classification_report(y_true, y_pred, target_names=CLASS_NAMES, zero_division=0))
    
    # ROC-AUC (one-vs-rest)
    try:
        y_bin = label_binarize(y_true, classes=list(range(NUM_CLASSES)))
        roc_auc = roc_auc_score(y_bin, y_probs, average='macro', multi_class='ovr')
        print(f"\nROC-AUC (macro, one-vs-rest): {roc_auc:.4f}")
    except Exception as e:
        print(f"\nROC-AUC calculation skipped: {str(e)}")
    
    print("\n" + "="*60)
    
    return accuracy, precision_macro, recall_macro, f1_macro


def plot_confusion_matrix(y_true, y_pred, output_path="confusion_matrix.png"):
    """Generate and save confusion matrix visualization"""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt='d',
        cmap='Blues',
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
        cbar_kws={'label': 'Count'}
    )
    plt.title('Confusion Matrix - Skin Lesion Classification', fontsize=14, fontweight='bold')
    plt.ylabel('True Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Confusion matrix saved to {output_path}")
    plt.close()


# ========== MAIN ==========

def main(args):
    """Main evaluation pipeline"""
    
    print("\n" + "="*60)
    print("SKIN LESION MODEL EVALUATION")
    print("="*60)
    
    # Load model
    print(f"\nBuilding ResNet18 (4 classes: {', '.join(CLASS_NAMES)})...")
    model = build_model()
    model = load_checkpoint(model, MODEL_PATH)
    model = model.to(DEVICE)
    model.eval()
    
    # Load dataset
    print(f"\nLoading test dataset from: {args.test_dir}")
    if not os.path.exists(args.test_dir):
        raise FileNotFoundError(f"Test directory not found: {args.test_dir}")
    
    test_dataset = ImageFolder(
        args.test_dir,
        transform=get_transforms()
    )
    
    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0
    )
    
    print(f"✓ Test set loaded: {len(test_dataset)} images")
    print(f"  Classes found: {test_dataset.classes}")
    
    # Evaluate
    print("\n" + "-"*60)
    print("Running evaluation...")
    print("-"*60)
    
    y_pred, y_true, y_probs = evaluate_model(model, test_loader)
    
    # Print metrics
    accuracy, precision, recall, f1 = print_metrics(y_true, y_pred, y_probs)
    
    # Plot confusion matrix
    plot_confusion_matrix(y_true, y_pred, args.output_cm)
    
    print("\n✓ Evaluation complete!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate skin lesion classification model"
    )
    parser.add_argument(
        "--test_dir",
        type=str,
        default="data/test",
        help="Path to test dataset (ImageFolder structure)"
    )
    parser.add_argument(
        "--output_cm",
        type=str,
        default="confusion_matrix.png",
        help="Output path for confusion matrix image"
    )
    
    args = parser.parse_args()
    
    try:
        main(args)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        exit(1)
