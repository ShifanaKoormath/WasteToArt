import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

# ---------------------------------------------------------
# Load model once at startup (best performance)
# ---------------------------------------------------------
MODEL_PATH = os.path.join(os.path.dirname(__file__), "biowaste_classifier.keras")
model = tf.keras.models.load_model(MODEL_PATH)

# Warm-up prediction (avoids first-call delay)
_dummy = np.zeros((1, 224, 224, 3), dtype=np.float32)
model.predict(_dummy)


# ---------------------------------------------------------
# Main prediction function used by pipeline
# ---------------------------------------------------------
def predict_class(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0

        prediction = model.predict(img_array, verbose=0)[0][0]
        label = "Biodegradable" if prediction < 0.5 else "Non-Biodegradable"
        return label

    except Exception as e:
        print(f"[ERROR] Failed to classify image {img_path}: {str(e)}")
        return "Unknown"
