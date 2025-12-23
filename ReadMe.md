🌱 Waste-to-Art Generator

Transform real-world waste images into AI-generated recycled artwork using a complete end-to-end pipeline:

Waste object detection (YOLOv8)

Biodegradability classification (CNN)

Automatic creative prompt generation

Stable Diffusion–based artwork generation

This project is designed for college-level demonstration and assumes no prior AI experience.

🔍 What This System Does

When a user uploads an image of waste:

Waste objects are detected

Each object is cropped

Objects are classified as Biodegradable / Non-Biodegradable

A creative prompt is automatically generated

Stable Diffusion creates a unique upcycled artwork

The final image is shown in the frontend

📁 Project Structure
WasteToArt/
├── backend/
│   ├── server.py
│   ├── pipeline.py
│   ├── uploads/                ← uploaded images
│   ├── output/                 ← generated artworks
│   ├── detection/
│   │   ├── detect.py
│   │   ├── yolov8s.pt
│   │   └── crops/              ← YOLO object crops
│   ├── classification/
│   │   ├── classify.py
│   │   └── biowaste_classifier.keras
│   ├── embedding/
│   │   └── text_embed.py
│   └── generation/
│       └── generate_art.py
│
└── frontend/
    └── index.html

🚀 Features

YOLOv8-based waste object detection

Automatic object cropping

Biodegradable vs non-biodegradable classification

AI-generated creative prompts

Stable Diffusion WebUI (API-based) image generation

Simple frontend with preview + final artwork

Full backend ↔ frontend integration

🧩 Technologies Used

Python 3.10+

Ultralytics YOLOv8

TensorFlow / Keras

Stable Diffusion WebUI (AUTOMATIC1111 API)

Flask

HTML / CSS / JavaScript

Sentence-Transformers (optional embeddings)

🔧 System Requirements
Minimum

Windows or Linux

Python 3.10

Git

8 GB RAM

Recommended (for Stable Diffusion)

GPU with 4 GB+ VRAM
(Intel / AMD / NVIDIA all supported via DirectML)

📦 Software Installation
Install Python 3.10

Download from:
https://www.python.org/downloads/release/python-3100/

⚠️ During installation:

✔ Check Add Python to PATH

🟩 SETUP STEPS (Follow in Order)
🟩 1. Create the Project Folder

Create a folder anywhere, e.g.:

WasteToArtProject


Open VS Code → File → Open Folder → WasteToArtProject

🟩 2. Open the Terminal

Inside VS Code:

Press Ctrl + `

Confirm you see:

PS C:\...\WasteToArtProject>

🟩 3. Clone the Repository
git clone https://github.com/ShifanaKoormath/WasteToArt.git
cd WasteToArt


Result:

WasteToArtProject/
└── WasteToArt/

🟩 4. Install Stable Diffusion WebUI (Intel DirectML)
Why this version?

No NVIDIA GPU required

Works on Intel, AMD, and many CPU-only systems

Download:
👉 https://github.com/lshqqytiger/stable-diffusion-webui-directml

Click Code → Download ZIP

Setup

Extract ZIP

Rename folder to:

stable-diffusion-webui


Move into project root:

WasteToArtProject/
├── WasteToArt/
└── stable-diffusion-webui/

🟩 5. Download Stable Diffusion Model (Required)

Model:

v1-5-pruned-emaonly.safetensors


Download:
👉 https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors

Place here:

stable-diffusion-webui/models/Stable-diffusion/

🟩 6. Enable API + Safe Precision Mode

Open:

stable-diffusion-webui/webui-user.bat


Replace contents with:

@echo off
set COMMANDLINE_ARGS=--api --precision full --no-half --no-half-vae
call webui.bat


Save and close.

🟩 7. Fix Float Precision Errors (CRITICAL)

After Stable Diffusion launches:

Open:

http://127.0.0.1:7860


Go to Settings → Optimizations

Enable:

✔ Upcast cross-attention to float32


Click Apply settings → Reload UI

⚠️ Skipping this is the #1 cause of crashes

🟩 8. Start Stable Diffusion
cd stable-diffusion-webui
.\webui-user.bat


Wait until:

Running on local URL: http://127.0.0.1:7860


✅ Keep this window running

🧪 9. Manual Stable Diffusion Test (MANDATORY)

Open:

http://127.0.0.1:7860


Paste this prompt exactly:

a simple recycled art sculpture made from plastic bottles, eco-friendly, minimal design, studio lighting


Leave defaults → Click Generate

✅ PASS CRITERIA

Image appears

Progress reaches 100%

No red terminal errors

❌ If this fails, STOP. Backend will not work.

🟩 10. Dataset Used

Dataset:
👉 https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification

Place inside:

backend/dataset/


Structure:

train/
val/


Prepare subset:

python backend/classification/prepare_subset.py


Train classifier:

python backend/classification/train_classifier.py

🟩 11. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

🟩 12. Start Backend Server
python backend/server.py


Expected:

Running on http://127.0.0.1:5000

🟩 13. Run Frontend

Open:

WasteToArt/frontend/index.html


Drag into Chrome.

Use images from:

sample_inputs/

🟦 System Pipeline Summary
Image Upload
   ↓
YOLO Detection
   ↓
Object Cropping
   ↓
Biodegradability Classification
   ↓
Prompt Generation
   ↓
Stable Diffusion
   ↓
Final Artwork

✅ Final Notes

Built for academic demonstration

Slow generation on CPU is expected

Stability matters more than speed
