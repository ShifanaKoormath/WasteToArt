import sys, os, uuid

# -----------------------------
# Path setup
# -----------------------------
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)
sys.path.append(PROJECT_ROOT)

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pipeline import process_image

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# -----------------------------
# Main processing endpoint
# -----------------------------
@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    save_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}.jpg")
    file.save(save_path)

    # -------- Read inputs from UI --------
    style = request.form.get("style")
    mood = request.form.get("mood")
    user_notes = request.form.get("notes")
    user_art_target = request.form.get("art_target")   # NEW (Hybrid override)

    try:
        result = process_image(
            save_path,
            return_path=True,
            style=style,
            mood=mood,
            user_notes=user_notes,
            user_art_target=user_art_target   # Pass to pipeline
        )

        # -----------------------------
        # Handle pipeline error cases
        # -----------------------------
        if isinstance(result, dict) and "error" in result:
            return jsonify(result), 200

        # -----------------------------
        # Success response
        # -----------------------------
        return jsonify({
            "image_path": result.get("image_path"),
            "generation_status": result.get("generation_status"),
            "prompt": result.get("prompt"),
            "negative_prompt": result.get("negative_prompt"),
            "reasoning": result.get("reasoning")
        }), 200

    except Exception as e:
        print("❌ SERVER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# -----------------------------
# Image serving endpoint
# -----------------------------
@app.route("/image/<filename>")
def get_image(filename):
    image_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404

    return send_file(image_path, mimetype="image/png")


# -----------------------------
# App runner
# -----------------------------
if __name__ == "__main__":
    app.run(port=5000)
