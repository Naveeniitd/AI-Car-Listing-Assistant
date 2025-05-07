import cv2
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
import numpy as np


class BackgroundValidator:
    def __init__(self):
        self.model = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")
        self.mask_generator = SamAutomaticMaskGenerator(self.model)
    
    def check_compliance(self, image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        masks = self.mask_generator.generate(image)
        
        # Simple check: if multiple distinct background segments exist
        bg_segments = len([m for m in masks if m['area'] > 0.2 * image.size])
        return {
            "is_compliant": bg_segments <= 1,
            "issues": ["Non-uniform background"] if bg_segments > 1 else []
        }