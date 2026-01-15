import sys, os, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detection.detect import run_detection
from classification.classify import predict_class
from prompt.prompt_builder import build_prompt
from generation.generate_art import generate_art


# -------------------------------
# Detection filtering rules
# -------------------------------
CONF_THRESHOLD = 0.5

ALLOWED_WASTE_CLASSES = {
    "bottle",
    "plastic bottle",
    "cup",
    "can",
    "paper",
    "cardboard",
    "plastic",
    "glass"
}


def process_image(
    input_image,
    return_path=False,
    style=None,
    mood=None,
    user_notes=None
):
    # -------------------------------
    # Reasoning (PER REQUEST)
    # -------------------------------
    reasoning = {
        "raw_detections": 0,
        "accepted_detections": 0,
        "rejected_detections": 0,
        "materials": {},
        "biodegradable": 0,
        "non_biodegradable": 0
    }

    print("\n🔍 Running YOLO Detection...")
    raw_detections = run_detection(input_image)
    reasoning["raw_detections"] = len(raw_detections)

    if len(raw_detections) == 0:
        return {
            "error": "NO_OBJECTS",
            "message": "No detectable objects found in the image."
        }

    # -------------------------------------------------
    # FILTER DETECTIONS
    # -------------------------------------------------
    detections = []

    print("\n🧹 Filtering detections...")
    for det in raw_detections:
        cls = det["class"].lower()
        conf = det["conf"]

        if conf < CONF_THRESHOLD:
            reasoning["rejected_detections"] += 1
            print(f"⚠ Ignored low-confidence: {cls} ({conf:.2f})")
            continue

        if cls not in ALLOWED_WASTE_CLASSES:
            reasoning["rejected_detections"] += 1
            print(f"⚠ Ignored non-waste class: {cls}")
            continue

        detections.append(det)

    reasoning["accepted_detections"] = len(detections)

    if len(detections) == 0:
        return {
            "error": "NO_OBJECTS",
            "message": "No valid waste objects detected after filtering."
        }

    print(f"\n✅ Accepted {len(detections)} waste object(s):")
    for det in detections:
        print(f" - {det['class']} (conf {det['conf']:.2f})")

    # -------------------------------------------------
    # Classification
    # -------------------------------------------------
    print("\n🧪 Running Classification...")

    biodegradable_count = 0
    non_biodegradable_count = 0

    for det in detections:
        label = predict_class(det["crop_path"])
        det["biodeg_label"] = label

        if label == "Biodegradable":
            biodegradable_count += 1
            reasoning["biodegradable"] += 1
        else:
            non_biodegradable_count += 1
            reasoning["non_biodegradable"] += 1

        material = det["class"]
        reasoning["materials"][material] = reasoning["materials"].get(material, 0) + 1

    print("\n📊 Classification Summary:")
    print(f"Biodegradable: {biodegradable_count}")
    print(f"Non-Biodegradable: {non_biodegradable_count}")

    if non_biodegradable_count == 0:
        return {
            "error": "NO_RECYCLABLES",
            "message": "Only biodegradable objects detected. No artwork generated."
        }

    # -------------------------------------------------
    # Prompt generation
    # -------------------------------------------------
    print("\n📝 Building FINAL PROMPT (backend-authoritative)...")

    prompt_text, negative_prompt = build_prompt(
        detections=detections,
        biodegradable_count=biodegradable_count,
        non_biodegradable_count=non_biodegradable_count,
        style=style,
        mood=mood,
        user_notes=user_notes
    )

    print("\nFINAL PROMPT:")
    print(prompt_text)

    # -------------------------------------------------
    # Stable Diffusion Generation
    # -------------------------------------------------
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}.png")

    print("\n🎨 Generating artwork...")
    generate_art(prompt_text, negative_prompt, output_path)

    print("\n✅ DONE! Image saved at:", output_path)

    # -------------------------------------------------
    # RETURN IMAGE + REASONING
    # -------------------------------------------------
    if return_path:
        return {
            "image_path": output_path,
            "reasoning": reasoning
        }

    return output_path
