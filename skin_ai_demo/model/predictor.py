# model/predictor.py

import torch
import torch.nn.functional as F

from utils.constants import LABEL_NAMES
from model.loader import DEVICE


def predict_image(model, image_tensor):
    """
    Runs inference and returns:
    - predicted class label
    - confidence score
    - raw predicted class index
    """

    image_tensor = image_tensor.to(DEVICE)

    with torch.no_grad():
        outputs = model(image_tensor)

        probabilities = F.softmax(outputs, dim=1)

        confidence, pred = torch.max(probabilities, 1)

    pred_index = pred.item()
    confidence_score = confidence.item()
    pred_label = LABEL_NAMES[pred_index]

    return {
        "label": pred_label,
        "confidence": confidence_score,
        "class_index": pred_index,
        "probabilities": probabilities.cpu().numpy()
    }