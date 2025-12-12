# pipeline/process.py
import os
import uuid
from detection.detect import run_detection
from classification.classify import infer_with_yolo_mapping
from generation.generate_art import generate_art

def build_prompt(detected_items, style="eco-art sculpture", arrangement=None):
    """
    detected_items: list of dicts returned by detect.run_detection
    style: optional art style
    arrangement: optional arrangement hint (robot, tree, abstract)
    """
    # count by class
    counts = {}
    for it in detected_items:
        cls = it.get("class", "object").lower()
        counts[cls] = counts.get(cls, 0) + 1

    parts = []
    for cls, cnt in counts.items():
        parts.append(f"{cnt} {cls}{'s' if cnt>1 else ''}")

    objects_text = ", ".join(parts) if parts else "various recycled objects"
    arrangement_text = f", arranged into a {arrangement}" if arrangement else ""
    prompt = (
        f"Create a creative upcycled artwork using {objects_text}{arrangement_text}. "
        f"The piece should emphasize sustainability and look handcrafted, imaginative and detailed. "
        f"Style: {style}. High detail, realistic textures of plastic and metal, studio lighting, sharp focus."
    )
    return prompt

def process_image(input_image):
    """
    Returns path to generated image.
    """
    # 1) Detect
    detected = run_detection(input_image)

    # 2) Classify / map to biodegradability
    items_with_labels = []
    for obj in detected:
        crop = obj["crop_path"]
        yolo_cls = obj.get("class", "")
        label, src = infer_with_yolo_mapping(yolo_cls, crop, prefer_yolo=True)
        items_with_labels.append({**obj, "biodeg_label": label, "label_source": src})

    # generate a quick summary for logging
    biodegradable = sum(1 for i in items_with_labels if i["biodeg_label"] == "Biodegradable")
    non_biodeg = sum(1 for i in items_with_labels if i["biodeg_label"] == "Non-Biodegradable")

    # 3) Build prompt
    prompt = build_prompt(detected, arrangement="futuristic sculpture")
    prompt += f" The sculpture should highlight that {non_biodeg} items are non-biodegradable and {biodegradable} are biodegradable."

    # 4) Generate art
    out_dir = os.path.join(os.path.dirname(__file__), "..", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{uuid.uuid4().hex}.png")

    generated = generate_art(prompt, out_path)
    return generated, {
        "prompt": prompt,
        "summary": {"biodegradable": biodegradable, "non_biodegradable": non_biodeg},
        "detected_items": items_with_labels
    }

if __name__ == "__main__":
    # quick local test
    img = "Plastic bottles.jpg"
    out, meta = process_image(img)
    print("Saved:", out)
    print("Meta:", meta)
