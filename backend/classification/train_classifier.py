import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

train_dir = "backend/dataset_cnn/train"
val_dir = "backend/dataset_cnn/val"

# -------------------------
# DATA GENERATORS (with augmentation)
# -------------------------
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True
)

val_datagen = ImageDataGenerator(rescale=1.0/255)

train_gen = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=16,
    class_mode="binary"
)

val_gen = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=16,
    class_mode="binary"
)

# -------------------------
# MODEL
# -------------------------
base = MobileNetV2(weights="imagenet", include_top=False)
base.trainable = False   # <-- CRUCIAL FIX

x = GlobalAveragePooling2D()(base.output)
x = Dropout(0.3)(x)
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base.input, outputs=output)

model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

# -------------------------
# TRAINING
# -------------------------
print("Training model...")
history = model.fit(
    train_gen,
    validation_data=val_gen,
    epochs=6,               # <-- Increased for stability
    verbose=1
)

# -------------------------
# SAVE MODEL
# -------------------------
model.save("backend/classification/biowaste_classifier.keras")
print("Model saved as biowaste_classifier.keras")
