import sys, os

# Fix import paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))  # backend/
PROJECT_ROOT = os.path.dirname(PROJECT_ROOT)               # project root
sys.path.append(PROJECT_ROOT)

from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

from pipeline import process_image
import uuid


app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.route("/process", methods=["POST"])
def process():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    save_path = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}.jpg")
    file.save(save_path)

    try:
        result = process_image(save_path, return_path=True)

        # -------------------------
        # Handle biodegradable-only case
        # -------------------------
        if isinstance(result, dict):
            if result.get("error") == "NO_RECYCLABLES":
                return jsonify(result), 200
            if result.get("error") == "NO_OBJECTS":
                return jsonify(result), 200

        # Otherwise result = image path
        output_path = os.path.abspath(result)
        print("➡ SENDING FILE:", output_path)

        return send_file(output_path, mimetype="image/png")

    except Exception as e:
        print("❌ SERVER ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
