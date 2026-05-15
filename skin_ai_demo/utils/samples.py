# samples.py - Sample images for demo mode

import io
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import random


def create_synthetic_sample_image(image_type: str = "nevus") -> Image.Image:
    """
    Create a synthetic dermoscopic-like image for demonstration.
    
    Args:
        image_type: One of "nevus", "melanoma", "bcc", "other"
    
    Returns:
        PIL Image (224x224 for model compatibility)
    """
    size = 224
    
    # Create base image with skin tone gradient
    img = Image.new('RGB', (size, size), color=(200, 140, 100))
    
    # Add subtle noise
    pixels = np.array(img).astype(float)
    noise = np.random.normal(0, 8, pixels.shape)
    pixels = np.clip(pixels + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(pixels)
    
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Draw lesion based on type
    if image_type == "nevus":
        # Benign nevus: well-defined, dark, round
        center = (112, 112)
        radius = 35
        color = (60, 50, 40, 180)
        draw.ellipse(
            [(center[0]-radius, center[1]-radius), (center[0]+radius, center[1]+radius)],
            fill=color
        )
        # Add subtle texture
        for _ in range(30):
            x = random.randint(center[0]-radius, center[0]+radius)
            y = random.randint(center[1]-radius, center[1]+radius)
            draw.point((x, y), fill=(80, 60, 50))
    
    elif image_type == "melanoma":
        # Suspicious melanoma: irregular, varied color, asymmetric
        # Main dark area
        draw.ellipse([(70, 80), (160, 170)], fill=(20, 10, 5, 200))
        # Irregular extensions
        for i in range(5):
            x = random.randint(50, 170)
            y = random.randint(60, 180)
            draw.ellipse([(x-15, y-15), (x+15, y+15)], fill=(40, 20, 10, 150))
        # Color variation (red area)
        draw.ellipse([(100, 100), (140, 130)], fill=(100, 30, 30, 120))
    
    elif image_type == "bcc":
        # BCC: pearlescent, raised-looking with irregular border
        center = (112, 112)
        radius = 40
        # Main lesion
        draw.ellipse(
            [(center[0]-radius, center[1]-radius), (center[0]+radius, center[1]+radius)],
            fill=(80, 60, 50, 160)
        )
        # Pearlescent effect - lighter areas
        for _ in range(15):
            x = random.randint(center[0]-radius, center[0]+radius)
            y = random.randint(center[1]-radius, center[1]+radius)
            draw.ellipse([(x-8, y-8), (x+8, y+8)], fill=(120, 100, 90, 100))
    
    else:  # other
        # Random asymmetric lesion
        draw.ellipse([(60, 80), (160, 150)], fill=(90, 70, 60, 150))
        draw.ellipse([(100, 120), (150, 180)], fill=(80, 50, 30, 150))
    
    img = img.filter(ImageFilter.GaussianBlur(radius=1.5))
    return img


def get_sample_images(limit: int = 4) -> dict:
    """
    Get a set of sample images for demo mode.
    
    Returns:
        Dict with image_type -> PIL Image
    """
    samples = {}
    types = ["nevus", "melanoma", "bcc", "other"]
    
    for img_type in types[:limit]:
        samples[img_type] = create_synthetic_sample_image(img_type)
    
    return samples


def get_sample_image_description(image_type: str) -> str:
    """Get clinical description of sample image type."""
    descriptions = {
        "nevus": "Common benign nevus - well-defined circular lesion",
        "melanoma": "Suspicious melanoma - irregular, varied pigmentation (ABCDE criteria positive)",
        "bcc": "Basal cell carcinoma - pearlescent appearance with irregular border",
        "other": "Miscellaneous benign lesion"
    }
    return descriptions.get(image_type, "Sample image")
