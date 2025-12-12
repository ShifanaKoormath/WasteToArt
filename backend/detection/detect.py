from ultralytics import YOLO
import os

def run_detection(image_path):
    model = YOLO("yolov8s.pt")  # using default model
    results = model(image_path)

    crop_dir = "backend/detection/crops"
    os.makedirs(crop_dir, exist_ok=True)

    saved_paths = []

    for r in results:
        if hasattr(r, "boxes"):
            for i, box in enumerate(r.boxes):
                # Crop each object and save
                crop = r.orig_img[
                    int(box.xyxy[0][1]): int(box.xyxy[0][3]),
                    int(box.xyxy[0][0]): int(box.xyxy[0][2])
                ]
                save_path = os.path.join(crop_dir, f"crop_{i}.jpg")
                import cv2
                cv2.imwrite(save_path, crop)
                saved_paths.append(save_path)

    return saved_paths
