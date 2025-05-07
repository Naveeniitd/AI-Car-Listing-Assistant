import cv2
import torch
from ultralytics.nn.tasks import DetectionModel
from torch.nn.modules.container import Sequential
torch.serialization.add_safe_globals([DetectionModel, Sequential])
from ultralytics import YOLO


class YOLODetector:
    def __init__(self):
        # Load pre-trained models (or your fine-tuned models)
        self.plate_model = YOLO("yolov8n.pt")  # Replace with custom trained model
        self.dent_model = YOLO("yolov8n.pt")   # Replace with custom trained model

    def detect_plates(self, image_path):
        """Detects license plates and blurs them"""
        img = cv2.imread(image_path)
        results = self.plate_model.predict(img)
        
        plates = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            plates.append({
                "bbox": [x1, y1, x2, y2],
                "confidence": float(box.conf[0])
            })
        
        return plates

    def detect_damage(self, image_path):
        """Detects dents/scratches"""
        img = cv2.imread(image_path)
        results = self.dent_model.predict(img)
        
        damages = []
        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            damages.append({
                "type": "dent",  # Replace with class names from your custom model
                "bbox": [x1, y1, x2, y2],
                "confidence": float(box.conf[0])
            })
        
        return damages