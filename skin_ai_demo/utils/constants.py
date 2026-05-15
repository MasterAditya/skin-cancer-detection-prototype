# utils/constants.py

LABEL_NAMES = ["nevus", "melanoma", "bcc", "other"]

MODEL_PATH = "skin_ai_demo/model/best_skin_model.pt"

APP_TITLE = "AI-Assisted Skin Lesion Risk Assessment System"

APP_SUBTITLE = (
    "Explainable Deep Learning Prototype for Dermatological Decision Support"
)

DISCLAIMER = (
    "Research prototype only. "
    "Not intended for clinical diagnosis or medical decision-making."
)

MODEL_INFO = {
    "Architecture": "ResNet18 (Transfer Learning)",
    "Validation Accuracy": "97.3%",
    "Datasets": "HAM10000 + ISIC2018 + Combined Skin Lesion Dataset",
    "Explainability": "Grad-CAM",
    "Risk Layer": "Rule-based Clinical Triage"
}

THRESHOLDS = {
    "melanoma_high": 85,
    "melanoma_moderate": 70,
    "bcc_high": 85,
    "nevus_low_risk": 90,
}