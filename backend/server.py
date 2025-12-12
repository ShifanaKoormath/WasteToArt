import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS

from pipeline import process_image
import uuid


app = Flask(__name__)
CORS(app)  # <-- THIS FIXES EVERYTHING

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
        output_path = process_image(save_path, return_path=True)

        # Make sure path is absolute
        output_path = os.path.abspath(output_path)

        print("➡ SENDING FILE:", output_path)

        return send_file(output_path, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
