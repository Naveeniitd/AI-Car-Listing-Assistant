import cv2
from app.services.image_processor import ImageProcessor

def test():
    processor = ImageProcessor()
    result = processor.process_image("/Users/naveen/Desktop/AI-Car-Listing-Assistant/car1.jpg")
    print(result)

if __name__ == "__main__":
    test()