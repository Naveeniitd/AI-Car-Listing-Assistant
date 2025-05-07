from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

class CarClassifier:
    def __init__(self):
        self.model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        self.processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        self.car_models = ["Toyota Camry", "Honda Civic", "Ford F-150"]  

    def predict_make_model(self, image_path):
        image = Image.open(image_path)
        inputs = self.processor(
            text=self.car_models,
            images=image,
            return_tensors="pt",
            padding=True
        )
        
        outputs = self.model(**inputs)
        probs = outputs.logits_per_image.softmax(dim=1)
        best_idx = probs.argmax().item()
        
        return {
            "make_model": self.car_models[best_idx],
            "confidence": probs[0][best_idx].item()
        }