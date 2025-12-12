🌱 Waste-to-Art — Full Setup Guide (Beginner Friendly)

This project turns real-world waste images into AI-generated recycled artwork using:

YOLO object detection

Biodegradability classification

Automatic prompt generation

Stable Diffusion image generation

This guide assumes zero prior experience.
Follow each step exactly.

🟩 1. Create a New Project Folder

Create a folder anywhere, for example:

WasteToArtProject


Open VS Code

Go to: File → Open Folder → select WasteToArtProject

🟩 2. Open the Terminal (PowerShell)

Inside VS Code:

👉 Press Ctrl + `
Make sure the terminal says:

PS C:\...WasteToArtProject>

🟩 3. Clone the Repository Into This Folder

In the terminal, run:

git clone https://github.com/ShifanaKoormath/WasteToArt.git


After cloning:

cd WasteToArt


Your structure now becomes:

WasteToArtProject/
    WasteToArt/   ← cloned repo

🟩 4. Download Stable Diffusion WebUI (Intel DirectML Version)

⚠️ IMPORTANT
This project works ONLY with the Intel DirectML version of Stable Diffusion
because it's compatible with all GPUs (Intel, AMD, basic laptop GPUs, even some CPUs).

Download here:

https://github.com/lshqqytiger/stable-diffusion-webui-directml

Click:

Code → Download ZIP


Extract the ZIP.

Rename the folder to:

stable-diffusion-webui


Now move this entire folder inside your project folder, like this:

WasteToArtProject/
    WasteToArt/
    stable-diffusion-webui/

🟩 5. Download a Stable Diffusion Model File

Stable Diffusion WILL NOT WORK without a model.

Recommended model (simple & lightweight):

💾 v1-5-pruned-emaonly.safetensors
Download:

https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors

After downloading:

Move it into:

stable-diffusion-webui/models/Stable-diffusion/


Folder must look like:

stable-diffusion-webui/
    models/
        Stable-diffusion/
            v1-5-pruned-emaonly.safetensors

🟩 6. Enable API + Safe Precision Settings

Open this file:

stable-diffusion-webui/webui-user.bat


Right-click → Edit

Replace ALL content with:

@echo off
set COMMANDLINE_ARGS=--api --precision full --no-half --no-half-vae
call webui.bat


Save & close.

🟩 7. IMPORTANT: Fix Float Precision Errors (Upcast Attention)

After Stable Diffusion launches:

Open the webpage:

http://127.0.0.1:7860


Go to Settings → Optimizations

Enable:

✔ Upcast cross-attention to float32

Click “Apply settings”

Click “Reload UI”

This prevents:

RuntimeError: Input type (float) and bias type (Half) should be the same

🟩 8. Start Stable Diffusion

Double-click:

stable-diffusion-webui/webui-user.bat


Wait until you see:

Running on local URL: http://127.0.0.1:7860


Keep this window open.

🟩 9. Backend Setup

In VS Code terminal:

cd WasteToArt/backend
python -m venv venv


Activate:

venv\Scripts\activate


Install dependencies:

pip install -r requirements.txt


If anything fails:

pip install flask flask-cors ultralytics tensorflow pillow numpy opencv-python sentence-transformers requests

🟩 10. Start the Backend Server

In the backend folder:

python server.py


You should see:

Running on http://127.0.0.1:5000


Backend ready ✔

🟩 11. Run the Frontend

No installation required.

Simply:

👉 Open the folder
👉 Go to:

WasteToArt/frontend/index.html


👉 Drag & drop into any browser (Chrome recommended)

Upload an image → the system will:

detect objects

classify biodegradable items

generate a creative prompt

call Stable Diffusion

display final artwork

🟦 12. How Everything Works Internally

1️⃣ Frontend sends uploaded image to backend
2️⃣ Backend saves it in /uploads
3️⃣ YOLO detects objects → crops saved in /detection/crops
4️⃣ Classifier determines biodegradable / non-biodegradable
5️⃣ Prompt is automatically generated
6️⃣ Backend sends prompt to Stable Diffusion API
7️⃣ SD generates artwork → saved in /backend/output
8️⃣ Frontend displays final AI art

🟦 13. Project Folder You Should Have
WasteToArtProject/
│
├── WasteToArt/                     ← cloned project
│   ├── backend/
│   ├── frontend/
│   └── README.md
│
└── stable-diffusion-webui/         ← Intel DirectML SD version
    ├── webui-user.bat
    └── models/
         └── Stable-diffusion/
               └── v1-5-pruned-emaonly.safetensors

🟦 14. COMMON ISSUES & FIXES
❌ SD API Not Found (404)

You forgot --api
Fix:

Open webui-user.bat → ensure:

--api

❌ Float / Half precision error

Fix (we already enabled):

✔ Upcast cross-attention
✔ --precision full
✔ --no-half
✔ --no-half-vae

❌ Blank output / no generation

Your model is in the wrong folder.

Model MUST be here:

stable-diffusion-webui/models/Stable-diffusion/

❌ Backend cannot find Stable Diffusion

Ensure SD is running on 127.0.0.1:7860