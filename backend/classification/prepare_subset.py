import os
import random
import shutil
from pathlib import Path

# ---------------------------------------------
# SOURCE DATASET LOCATION (your actual dataset)
# ---------------------------------------------
SRC_TRAIN_BIO = Path("backend/dataset/train/biodegradable")
SRC_TRAIN_NON = Path("backend/dataset/train/non_biodegradable")

SRC_VAL_BIO = Path("backend/dataset/val/biodegradable")
SRC_VAL_NON = Path("backend/dataset/val/non_biodegradable")

# ---------------------------------------------
# TARGET (subset) dataset
# ---------------------------------------------
DST_TRAIN_BIO = Path("backend/dataset_cnn/train/biodegradable")
DST_TRAIN_NON = Path("backend/dataset_cnn/train/non_biodegradable")

DST_VAL_BIO = Path("backend/dataset_cnn/val/biodegradable")
DST_VAL_NON = Path("backend/dataset_cnn/val/non_biodegradable")

# ---------------------------------------------
# HOW MANY IMAGES YOU WANT IN SUBSET
# ---------------------------------------------
TRAIN_COUNT = 960
VAL_COUNT = 240


def select_and_copy(src, dst, max_count):
    files = [f for f in os.listdir(src) if f.lower().endswith((".jpg", ".png", ".jpeg"))]
    random.shuffle(files)
    selected = files[:max_count]

    for f in selected:
        shutil.copy(src / f, dst / f)


def ensure_dirs():
    for d in [DST_TRAIN_BIO, DST_TRAIN_NON, DST_VAL_BIO, DST_VAL_NON]:
        os.makedirs(d, exist_ok=True)


# ---------------------------------------------
# MAIN
# ---------------------------------------------
ensure_dirs()

print("📦 Creating TRAIN subset (biodegradable)...")
select_and_copy(SRC_TRAIN_BIO, DST_TRAIN_BIO, TRAIN_COUNT)

print("📦 Creating TRAIN subset (non-biodegradable)...")
select_and_copy(SRC_TRAIN_NON, DST_TRAIN_NON, TRAIN_COUNT)

print("📦 Creating VAL subset (biodegradable)...")
select_and_copy(SRC_VAL_BIO, DST_VAL_BIO, VAL_COUNT)

print("📦 Creating VAL subset (non-biodegradable)...")
select_and_copy(SRC_VAL_NON, DST_VAL_NON, VAL_COUNT)

print("\n🎉 Subset creation complete!")
