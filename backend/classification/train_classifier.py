import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

train_dir = "backend/dataset_cnn/train"
val_dir = "backend/dataset_cnn/val"

# -------------------------
# DATA GENERATORS
# -------------------------
datagen = ImageDataGenerator(rescale=1.0/255)

train_gen = datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=8,
    class_mode="binary"      # **** FIXED ****
)

val_gen = datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=8,
    class_mode="binary"      # **** FIXED ****
)

# -------------------------
# MODEL
# -------------------------
base = MobileNetV2(weights="imagenet", include_top=False)
x = GlobalAveragePooling2D()(base.output)
output = Dense(1, activation="sigmoid")(x)   # **** FIXED ****

model = Model(inputs=base.input, outputs=output)

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

print("Training model...")
model.fit(train_gen, validation_data=val_gen, epochs=3)

# -------------------------
# SAVE MODEL
# -------------------------
model.save("backend/classification/biowaste_classifier.keras")

print("Model saved as biowaste_classifier.keras")
