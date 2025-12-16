

# 🌱 Waste-to-Art Generator

**An Explainable AI System for Transforming Waste into Digital Art**

The Waste-to-Art Generator is an end-to-end AI system that transforms images of real-world waste into creative, upcycled digital artwork.
It combines computer vision, material classification, and generative AI with a focus on **interpretability, sustainability awareness, and academic clarity**.

This project is designed for **college-level demonstration**, emphasizing how AI systems reason step-by-step rather than acting as black boxes.

---

## 🔍 What This System Does

When a user uploads an image containing waste materials:

1. Waste objects are detected from the image
2. Low-confidence and irrelevant detections are filtered
3. Detected objects are classified as biodegradable or non-biodegradable
4. A structured creative prompt is generated based on detected materials and quantity
5. A generative model creates an upcycled artwork concept
6. The final artwork is displayed with an **AI reasoning summary explaining the process**

The system prioritizes **accuracy, transparency, and stability over raw speed**.

---

## 🧠 Explainable AI Focus (New)

Unlike basic image-to-image demos, this system includes an **AI Reasoning Summary** in the frontend that explains:

* How objects were detected and filtered
* How materials were classified
* How the creative concept was formed
* What the final artwork represents

The reasoning is presented in **plain language**, without mentioning internal model or framework names, making it suitable for non-technical evaluators.

---

## 🎨 Frontend Capabilities (Updated)

The frontend now provides:

* Image upload with live preview
* Optional creative controls:

  * Art style (e.g., minimalist, abstract, handcrafted)
  * Mood (e.g., calm, hopeful, earthy)
  * Short creative notes (style-only guidance)
* A redesigned sustainability insight panel shown during processing
* Final artwork display with:

  * Download Artwork button
  * Collapsible AI Reasoning Summary

The UI is intentionally calm and minimal to keep focus on the artwork and reasoning.

---

## 📁 Project Structure

```
WasteToArt/
├── backend/
│   ├── server.py              # API + image serving
│   ├── pipeline.py            # End-to-end processing logic
│   ├── uploads/               # Uploaded images
│   ├── output/                # Generated artworks
│   ├── detection/
│   │   ├── detect.py
│   │   ├── yolov8s.pt
│   │   └── crops/
│   ├── classification/
│   │   ├── classify.py
│   │   └── biowaste_classifier.keras
│   ├── prompt/
│   │   └── prompt_builder.py  # Backend-authoritative prompt logic
│   └── generation/
│       └── generate_art.py
│
└── frontend/
    └── index.html              # Interactive UI + explainability
```

---

## 🚀 Key Features

* Waste object detection with confidence filtering
* Automatic object cropping
* Biodegradable vs non-biodegradable classification
* Backend-controlled creative prompt generation
* Quantity-aware material interpretation (e.g., multiple bottles → reusable objects)
* Stable Diffusion–based artwork generation (API-driven)
* Explainable AI reasoning summary
* Downloadable final artwork
* Clean backend ↔ frontend API separation

---

## 🧩 Technologies Used

* Python 3.10+
* Ultralytics YOLOv8
* TensorFlow / Keras
* Stable Diffusion WebUI (AUTOMATIC1111 API)
* Flask
* HTML / CSS / JavaScript

*(Embeddings are optional and used only for internal prompt refinement.)*

---

## 🔧 System Requirements

### Minimum

* Windows or Linux
* Python 3.10
* Git
* 8 GB RAM

### Recommended (for Stable Diffusion)

* GPU with 4 GB+ VRAM
* Intel / AMD / NVIDIA supported via DirectML

---

## 📦 Software Installation

### Install Python 3.10

Download from:
[https://www.python.org/downloads/release/python-3100/](https://www.python.org/downloads/release/python-3100/)

During installation:
✔ Check **Add Python to PATH**

---

## 🟩 Setup Steps (Follow in Order)

### 1. Create the Project Folder

```
WasteToArtProject
```

Open in VS Code.

---

### 2. Open the Terminal

Press `Ctrl + ``
Confirm:

```
PS C:\...\WasteToArtProject>
```

---

### 3. Clone the Repository

```bash
git clone https://github.com/ShifanaKoormath/WasteToArt.git
cd WasteToArt
```

---

### 4. Install Stable Diffusion WebUI (DirectML)

This version works without NVIDIA GPUs.

Download:
[https://github.com/lshqqytiger/stable-diffusion-webui-directml](https://github.com/lshqqytiger/stable-diffusion-webui-directml)

Extract and rename to:

```
stable-diffusion-webui
```

Project structure:

```
WasteToArtProject/
├── WasteToArt/
└── stable-diffusion-webui/
```

---

### 5. Download Stable Diffusion Model

Model:

```
v1-5-pruned-emaonly.safetensors
```

Place in:

```
stable-diffusion-webui/models/Stable-diffusion/
```

---

### 6. Enable API + Safe Precision Mode

Edit:

```
stable-diffusion-webui/webui-user.bat
```

Replace contents:

```bat
@echo off
set COMMANDLINE_ARGS=--api --precision full --no-half --no-half-vae
call webui.bat
```

---

### 7. Fix Float Precision Errors (CRITICAL)

After launch, open:

```
http://127.0.0.1:7860
```

Settings → Optimizations → Enable:
✔ Upcast cross-attention to float32

Apply and reload.

---

### 8. Start Stable Diffusion

```bash
cd stable-diffusion-webui
.\webui-user.bat
```

Keep this window running.

---

### 9. Manual Stable Diffusion Test (MANDATORY)

Prompt:

```
a simple recycled art sculpture made from plastic bottles,
eco-friendly, minimal design, studio lighting
```

If this fails, stop — backend will not work.

---

### 10. Dataset Used (Optional Training)

Dataset:
[https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification](https://www.kaggle.com/datasets/asdasdasasdas/garbage-classification)

Structure:

```
backend/dataset/
 ├── train/
 └── val/
```

Prepare subset:

```bash
python backend/classification/prepare_subset.py
```

Train classifier:

```bash
python backend/classification/train_classifier.py
```

---

### 11. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

### 12. Start Backend Server

```bash
python backend/server.py
```

Expected:

```
Running on http://127.0.0.1:5000
```

---

### 13. Run Frontend

Open:

```
frontend/index.html
```

Use a modern browser (Chrome recommended).

---

## 🟦 System Pipeline Summary

```
Image Upload
   ↓
Object Detection
   ↓
Confidence Filtering
   ↓
Material Classification
   ↓
Creative Prompt Construction
   ↓
Artwork Generation
   ↓
Explainable Result + Download
```

---

## ⚠️ Limitations

* Detection accuracy depends on image clarity and lighting
* Transparent plastics may reduce confidence scores
* Artwork is conceptual and digitally generated
* CPU-only systems will experience slower generation

---

## ✅ Final Notes

* Built for academic demonstration
* Emphasizes **interpretability and reasoning**
* Stability and clarity matter more than speed

---

