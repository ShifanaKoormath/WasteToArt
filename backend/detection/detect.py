# backend/detection/detect.py

import os
import uuid
import cv2
from ultralytics import YOLO

MODEL = YOLO("yolov8n.pt")  # lightweight + fast

# -------------------------------
# BIODEGRADABLE (organic waste)
# -------------------------------
ORGANIC_CLASSES = {
    "banana",
    "apple",
    "orange",
    "carrot",
    "broccoli",
    "hot dog",
    "sandwich",
    "pizza",
    "donut",
    "cake",
    "potted plant",
    "book",      # paper-based (biodegradable)
    "paper"
}

# -------------------------------
# NON-BIODEGRADABLE (plastic, metal, etc.)
# -------------------------------
NONBIO_CLASSES = {
    "bottle",
    "cup",
    "can",
    "plastic",
    "box",
    "carton",
    "tin",
    "bag",
    "container",
    "bowl"
}

# Merge all allowed waste classes
VALID_CLASSES = ORGANIC_CLASSES.union(NONBIO_CLASSES)


def run_detection(image_path):

    results = MODEL(image_path)[0]

    crop_dir = "backend/detection/crops"
    os.makedirs(crop_dir, exist_ok=True)

    detections = []

    for box in results.boxes:
        cls_id = int(box.cls[0])
        cls_name = results.names[cls_id].lower()
        conf = float(box.conf[0])

        # Filter out unrelated classes
        if cls_name not in VALID_CLASSES:
            continue

        # Confidence threshold
        if conf < 0.30:
            continue

        # Clean cropping
        x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
        crop = results.orig_img[y1:y2, x1:x2]

        crop_path = os.path.join(crop_dir, f"{uuid.uuid4().hex}.jpg")
        cv2.imwrite(crop_path, crop)

        detections.append({
            "class": cls_name,
            "conf": conf,
            "crop_path": crop_path
        })

    return detections
