import streamlit as st
from io import BytesIO
from collections import Counter

import numpy as np
from PIL import Image

import torch
from ultralytics import YOLO
from diffusers import StableDiffusionPipeline
from sentence_transformers import SentenceTransformer


# ----------------- Page config -----------------
st.set_page_config(
    page_title="Waste-to-Art Generator",
    page_icon="♻️",
    layout="centered",
)

st.title("♻️ Waste-to-Art Generator 🎨")
st.caption("Waste-to-Art Team Project")

st.write(
    "Upload a household waste image and describe a creative idea. "
    "The system detects waste objects and generates an upcycled art concept using Stable Diffusion."
)


# ----------------- Cached model loaders -----------------
@st.cache_resource
def load_yolo():
    return YOLO("yolov8m.pt")   # will auto-download the first time


@st.cache_resource
def load_text_model():
    return SentenceTransformer("paraphrase-MiniLM-L6-v2")


@st.cache_resource
def load_sd15():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    return pipe, device


# ----------------- Helper: describe detected objects -----------------
WASTE_KEYWORDS = [
    "bottle",
    "cup",
    "can",
    "bowl",
    "vase",
    "box",
    "carton",
    "bag",
    "fork",
    "knife",
    "spoon",
    "book",
    "paper",
]


def summarize_objects(class_ids, class_names):
    labels = [class_names[int(i)] for i in class_ids]
    # keep only waste-like labels
    filtered = [lbl for lbl in labels if any(k in lbl.lower() for k in WASTE_KEYWORDS)]
    if not filtered:
        return "various household waste objects"

    counts = Counter(filtered)
    parts = []
    for lbl, c in counts.items():
        name = lbl.lower()
        if c == 1:
            parts.append(f"1 {name}")
        else:
            parts.append(f"{c} {name}s")
    return ", ".join(parts)


# ----------------- UI inputs -----------------
uploaded_file = st.file_uploader("Upload waste image", type=["jpg", "jpeg", "png"])
user_prompt = st.text_input(
    "Enter creative prompt",
    placeholder="e.g. Modern flower vase design using recycled plastic bottles with vibrant patterns",
)

generate_clicked = st.button("Generate Art Idea ✨")

# ----------------- Main logic -----------------
if generate_clicked:
    if uploaded_file is None:
        st.error("Please upload an image of waste materials.")
        st.stop()
    if not user_prompt.strip():
        st.error("Please enter a creative prompt.")
        st.stop()

    # Read image
    pil_img = Image.open(uploaded_file).convert("RGB")
    img_np = np.array(pil_img)

    # Load models lazily
    with st.spinner("Loading models (first time can take a bit)..."):
        yolo_model = load_yolo()
        text_model = load_text_model()
        sd_pipe, device = load_sd15()

    # YOLO detection
    with st.spinner("Detecting waste objects..."):
        results = yolo_model(img_np)
        result = results[0]
        det_img = result.plot()  # BGR numpy

        class_ids = result.boxes.cls.cpu().numpy() if result.boxes is not None else []
        obj_summary = summarize_objects(class_ids, yolo_model.names)

    st.subheader("Detected Waste Objects")
    st.image(det_img, caption=f"Detected objects: {obj_summary}", use_column_width=True)

    # SBERT embedding (for report / architecture – not strictly needed at inference)
    with st.spinner("Encoding creative prompt (SBERT)..."):
        text_emb = text_model.encode([user_prompt])[0]  # (384,)
    st.caption(f"Prompt embedding length (SBERT MiniLM): {len(text_emb)}")

    # Build final prompt for Stable Diffusion
    final_prompt = (
        f"{user_prompt}, using {obj_summary}, eco-friendly recycled craft design, "
        f"upcycled art, highly detailed, professional product photography, soft lighting"
    )

    st.subheader("Final Prompt Sent to Generator")
    st.write(final_prompt)

    # Generate art
    with st.spinner("Generating upcycled art idea with Stable Diffusion v1.5..."):
        image = sd_pipe(
            final_prompt,
            num_inference_steps=25,
            guidance_scale=7.5,
        ).images[0]

    st.subheader("Generated Waste-to-Art Idea")
    st.image(image, use_column_width=True)
    st.success("Generation complete!")


st.markdown("---")
st.caption(
    "This is a research prototype for demonstrating a deep-learning based waste-to-art idea generator."
)
