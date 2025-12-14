# pipeline_code/inference.py

from ultralytics import YOLO
import torch
import cv2

class SolarPanelDetector:
    def __init__(self, model_path, conf_threshold=0.3):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = YOLO(model_path)
        self.model.to(self.device)
        self.conf_threshold = conf_threshold

    def predict(self, image_path):
        """
        Runs inference on a single image.

        Returns:
        [
            {
                "bbox": [x1, y1, x2, y2],
                "confidence": float,
                "class": "solar_panel"
            },
            ...
        ]
        """
        results = self.model(
            image_path,
            conf=self.conf_threshold,
            device=self.device,
            verbose=False
        )[0]

        detections = []

        for box in results.boxes:
            detections.append({
                "bbox": box.xyxy.cpu().numpy().tolist()[0],
                "confidence": float(box.conf.cpu().numpy()),
                "class": "solar_panel"
            })

        return detections
