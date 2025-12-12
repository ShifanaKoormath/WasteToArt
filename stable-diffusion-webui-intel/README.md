🌱 Waste-to-Art Generator

Turn real-world waste images into AI-generated recycled artwork using YOLO object detection, biodegradability classification, and Stable Diffusion prompt-based generation.

This project analyzes uploaded waste images, detects objects, classifies each into Biodegradable / Non-Biodegradable, generates a creative prompt, and uses Stable Diffusion to generate a unique upcycled artwork.

📁 Project Structure

Waste-to-Art/
│
├── backend/
│   ├── server.py
│   ├── pipeline.py
│   ├── output/               ← generated images saved here
│   ├── uploads/              ← uploaded images
│   ├── detection/
│   │   ├── detect.py
│   │   ├── yolov8s.pt
│   │   └── crops/            ← YOLO object crops
│   ├── classification/
│   │   ├── classify.py
│   │   └── biowaste_classifier.keras
│   ├── embedding/
│   │   └── text_embed.py
│   ├── generation/
│       └── generate_art.py
│
└── frontend/
    └── index.html

🚀 Features

Waste object detection using YOLOv8

Cropping each detected object

Biodegradable vs Non-Biodegradable classification

Automatic prompt construction

Stable Diffusion WebUI → final art generation

Clean, simple frontend with preview & generated artwork

Full backend–frontend integration

🧩 Technologies Used

Python 3.10+

Ultralytics YOLOv8 for object detection

TensorFlow/Keras for biodegradability classification

Stable Diffusion WebUI API (AUTOMATIC1111) for art generation

Flask backend

HTML/CSS/JS frontend

Sentence-Transformers for embeddings (optional)

🔧 1. System Requirements

Minimum recommended:

Windows / Linux

Python 3.10

GPU with 4GB+ VRAM (recommended for Stable Diffusion)

Installed:

Git

Stable Diffusion WebUI (AUTOMATIC1111)

📦 2. Install Required Software
Install Python 3.10

Download from:
https://www.python.org/downloads/release/python-3100/

During installation → check “Add Python to PATH”

📥 3. Clone the Repository
git clone https://github.com/<your-repo>/Waste-to-Art.git
cd Waste-to-Art

🐍 4. Create Virtual Environment & Install Dependencies
cd backend
python -m venv venv
venv\Scripts\activate       # Windows
# or source venv/bin/activate for Linux

pip install -r requirements.txt


If you don't have a requirements.txt, create one:

flask
flask-cors
ultralytics
tensorflow
pillow
numpy
requests
sentence-transformers
opencv-python

🎨 5. Install Stable Diffusion WebUI (AUTOMATIC1111)
Download:

https://github.com/AUTOMATIC1111/stable-diffusion-webui

Steps:

Extract the zip

Run:

webui-user.bat


After it launches once → Close it

Enable the API:

Open webui-user.bat in Notepad and add:

set COMMANDLINE_ARGS=--api


Run again:

webui-user.bat


Stable Diffusion will now run at:

http://127.0.0.1:7860

🤖 6. Download YOLO Model

Inside /backend/detection/ place:

yolov8s.pt


If missing:

yolo download model=yolov8s.pt

🧠 7. Add Your Biodegradability Classifier

Place your trained:

biowaste_classifier.keras


inside:

backend/classification/

🛠️ 8. Backend Setup

Verify folder structure exactly:

backend/
    server.py
    pipeline.py
    detection/detect.py
    classification/classify.py
    generation/generate_art.py


Run backend:

venv\Scripts\activate
python server.py


You should see:

Running on http://127.0.0.1:5000

🌐 9. Frontend Setup

You must NOT open index.html by double-clicking.
That results in:

origin: null
CORS error


Instead, run a local server:

cd frontend
python -m http.server 8080


Open:

http://localhost:8080/index.html

🔥 10. How the System Works (Pipeline)

User uploads an image through frontend

Backend receives it → saves to /backend/uploads

YOLO detects objects → saves crops to /backend/detection/crops

Each crop → classification model → Biodegradable/Non

Backend counts materials

Creates a prompt dynamically

Sends prompt to Stable Diffusion API

SD generates art → saved to /backend/output

Backend returns PNG → frontend displays it

▶️ 11. Running the Full System
Step 1 — Start Stable Diffusion API
webui-user.bat


Ensure it shows:

Running on local URL: http://127.0.0.1:7860

Step 2 — Start Backend
cd backend
venv\Scripts\activate
python server.py

Step 3 — Start Frontend
cd frontend
python -m http.server 8080

Step 4 — Open Browser
http://localhost:8080/index.html


Upload a waste image → wait → see generated artwork.

🧯 12. Common Errors & Fixes
❌ CORS Error
No Access-Control-Allow-Origin


Fix: in server.py add:

from flask_cors import CORS
CORS(app)

❌ FileNotFoundError: backend/backend/output…

Cause:
Relative paths doubling folder names.

Fix:
Use absolute paths in pipeline.py and server.py:

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

❌ SD API timeout or 500 error

Fix:

Ensure --api is enabled

Test manually:

http://127.0.0.1:7860/docs

❌ No image generated

Increase SD steps:

"steps": 20


Or enable a valid model in SD WebUI.

🧭 13. Future Improvements

Add live progress updates (SSE/Websocket)

Filter out irrelevant YOLO classes

Add better prompt generator

Train a custom waste detector

Improve UI

🎉 14. Credits

Developed by: Shifana K
Guide: Waste-to-Art AI pipeline using YOLO + Keras + Stable Diffusion