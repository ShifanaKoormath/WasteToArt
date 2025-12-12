import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

# Load model safely regardless of where script is executed
MODEL_PATH = os.path.join(os.path.dirname(__file__), "biowaste_classifier.keras")
model = tf.keras.models.load_model(MODEL_PATH)

# Test image path (use your cropped detection output)
TEST_IMAGE = "backend/detection/crops/crop_0.jpg"

def predict(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    
    prediction = model.predict(img_array)[0][0]
    
    label = "Biodegradable" if prediction < 0.5 else "Non-Biodegradable"
    
    print(f"\nImage: {img_path}")
    print(f"Prediction score: {prediction:.4f}")
    print(f"Predicted Class: {label}")

predict(TEST_IMAGE)
def predict_class(img_path):
    img = image.load_img(img_path, target_size=(224,224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)[0][0]
    label = "Biodegradable" if prediction < 0.5 else "Non-Biodegradable"
    return label
