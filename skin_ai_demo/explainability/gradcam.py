# explainability/gradcam.py

import torch
import torch.nn.functional as F
import numpy as np
import cv2


class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer

        self.gradients = None
        self.activations = None

        self._register_hooks()

    def _register_hooks(self):
        def forward_hook(module, input, output):
            self.activations = output

        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]

        self.target_layer.register_forward_hook(forward_hook)
        self.target_layer.register_full_backward_hook(backward_hook)

    def generate(self, image_tensor, class_index):
        """
        Generate Grad-CAM heatmap
        """

        self.model.zero_grad()

        output = self.model(image_tensor)

        output[0, class_index].backward()

        pooled_gradients = torch.mean(
            self.gradients,
            dim=[0, 2, 3]
        )

        activations = self.activations.detach()

        for i in range(activations.shape[1]):
            activations[:, i, :, :] *= pooled_gradients[i]

        heatmap = torch.mean(activations, dim=1).squeeze()

        heatmap = F.relu(heatmap)

        heatmap /= torch.max(heatmap)

        heatmap = heatmap.cpu().numpy()

        return heatmap


def overlay_heatmap(original_image, heatmap):
    """
    Overlay Grad-CAM heatmap on original image
    """

    img_np = np.array(original_image)

    heatmap = cv2.resize(
        heatmap,
        (img_np.shape[1], img_np.shape[0])
    )

    heatmap = np.uint8(255 * heatmap)

    heatmap = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    heatmap = cv2.cvtColor(
        heatmap,
        cv2.COLOR_BGR2RGB
    )

    overlay = heatmap * 0.4 + img_np

    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    return overlay