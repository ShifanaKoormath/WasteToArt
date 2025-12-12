import os
import shutil
import random
import requests
from pathlib import Path

# -------------------------
# CONFIG
# -------------------------
BIO_URLS = [
    # biodegradable
    "https://images.pexels.com/photos/615705/pexels-photo-615705.jpeg",
    "https://images.pexels.com/photos/65133/pexels-photo-65133.jpeg",
    "https://images.pexels.com/photos/892670/pexels-photo-892670.jpeg",
    "https://images.pexels.com/photos/1673775/pexels-photo-1673775.jpeg",
    "https://images.pexels.com/photos/3962285/pexels-photo-3962285.jpeg",
]

NONBIO_URLS = [
    # non biodegradable
    "https://images.pexels.com/photos/802221/pexels-photo-802221.jpeg",
    "https://images.pexels.com/photos/3735217/pexels-photo-3735217.jpeg",
    "https://images.pexels.com/photos/2566573/pexels-photo-2566573.jpeg",
    "https://images.pexels.com/photos/3735215/pexels-photo-3735215.jpeg",
    "https://images.pexels.com/photos/623182/pexels-photo-623182.jpeg",
]

BASE_DIR = Path("backend/dataset_cnn")
TRAIN_BIO = BASE_DIR / "train" / "biodegradable"
TRAIN_NON = BASE_DIR / "train" / "non_biodegradable"
VAL_BIO = BASE_DIR / "val" / "biodegradable"
VAL_NON = BASE_DIR / "val" / "non_biodegradable"

# -------------------------
# FUNCTIONS
# -------------------------

def download_image(url, dest):
    """Download an image safely."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                f.write(r.content)
            print("Downloaded:", dest)
        else:
            print("Failed:", url)
    except Exception as e:
        print("ERROR downloading", url, e)

def make_dirs():
    for d in [TRAIN_BIO, TRAIN_NON, VAL_BIO, VAL_NON]:
        os.makedirs(d, exist_ok=True)

def save_images(urls, train_dir, val_dir):
    random.shuffle(urls)
    split = int(len(urls) * 0.8)
    train_urls = urls[:split]
    val_urls = urls[split:]

    for i, url in enumerate(train_urls):
        download_image(url, train_dir / f"img_{i}.jpg")

    for i, url in enumerate(val_urls):
        download_image(url, val_dir / f"img_{i}.jpg")

# -------------------------
# MAIN
# -------------------------

print("Creating dataset folders...")
make_dirs()

print("\nDownloading biodegradable...")
save_images(BIO_URLS, TRAIN_BIO, VAL_BIO)

print("\nDownloading non-biodegradable...")
save_images(NONBIO_URLS, TRAIN_NON, VAL_NON)

print("\nDataset build complete!")
