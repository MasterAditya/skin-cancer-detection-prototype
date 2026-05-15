# model/loader.py

import torch
from torchvision.models import resnet18

from utils.constants import MODEL_PATH


DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


@torch.no_grad()
def load_model():
    """
    Reconstruct model architecture
    Load trained checkpoint
    Move to device
    """

    model = resnet18(weights=None)

    model.fc = torch.nn.Linear(
        model.fc.in_features,
        4
    )

    model.load_state_dict(
        torch.load(MODEL_PATH, map_location=DEVICE)
    )

    model = model.to(DEVICE)
    model.eval()

    return model