import cv2
from app.image_processing.yolo_detector import YOLODetector
from app.image_processing.clip_classifier import CarClassifier
from app.image_processing.background_check import BackgroundValidator

class ImageProcessor:
    def __init__(self):
        self.yolo = YOLODetector()
        self.clip = CarClassifier()
        self.bg_check = BackgroundValidator()

    def process_image(self, image_path):
        # Process all components
        results = {
            "license_plates": self.yolo.detect_plates(image_path),
            "damages": self.yolo.detect_damage(image_path),
            "make_model": self.clip.predict_make_model(image_path),
            "background_check": self.bg_check.check_compliance(image_path)
        }
        
        # Basic color detection (example)
        img = cv2.imread(image_path)
        avg_hsv = cv2.mean(cv2.cvtColor(img, cv2.COLOR_BGR2HSV))
        results["color"] = self._hsv_to_color_name(avg_hsv)
        
        return results

    def _hsv_to_color_name(self, hsv):
        # Implement your color mapping logic
        hue = hsv[0]
        if hue < 15: return "red"
        elif hue < 45: return "orange"
        # ... add more color ranges
        return "unknown"