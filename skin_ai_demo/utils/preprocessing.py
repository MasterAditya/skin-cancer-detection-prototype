# utils/preprocessing.py

from PIL import Image
from torchvision import transforms


def get_transforms():
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])


def preprocess_image(uploaded_file):
    """
    Takes uploaded image file and returns:
    - original PIL image
    - transformed tensor ready for model
    """

    image = Image.open(uploaded_file).convert("RGB")

    transform = get_transforms()

    tensor = transform(image).unsqueeze(0)

    return image, tensor