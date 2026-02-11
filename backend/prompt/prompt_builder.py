import re
from collections import Counter


# -------------------------------
# Guardrails
# -------------------------------

FORBIDDEN_KEYWORDS = [
    "human", "person", "face", "animal", "dragon", "monster",
    "weapon", "gun", "blood", "war", "car", "bike", "building",
    "gold", "diamond", "space", "galaxy"
]

MAX_USER_TEXT_LEN = 120


def sanitize_user_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()[:MAX_USER_TEXT_LEN]

    for word in FORBIDDEN_KEYWORDS:
        text = re.sub(rf"\b{word}\b", "", text)

    return text.strip()


# -------------------------------
# Composition Logic
# -------------------------------

def choose_composition(count):
    if count == 1:
        return "a handcrafted artistic transformation"
    elif count <= 3:
        return "a small assembled recycled artwork"
    elif count <= 6:
        return "a structured recycled art composition"
    else:
        return "a layered clustered recycled artwork"


# -------------------------------
# Material → Texture
# -------------------------------

MATERIAL_TEXTURE_MAP = {
    "bottle": "recycled translucent plastic texture",
    "plastic": "recycled plastic surface",
    "can": "recycled aluminum metal texture",
    "tin": "brushed metal surface",
    "glass": "recycled reflective glass texture",
    "paper": "recycled paper texture",
    "cardboard": "corrugated cardboard texture"
}


# -------------------------------
# Object → Shape grounding
# -------------------------------

OBJECT_SHAPE_MAP = {
    "bottle": "cylindrical bottle-like form",
    "cup": "curved cup-like form",
    "can": "cylindrical can-like form",
    "glass": "rounded glass-like form",
    "paper": "flat layered sheet-like form",
    "cardboard": "layered structural form",
    "box": "rectangular geometric form"
}


# -------------------------------
# Shape orientation from bbox
# -------------------------------

def extract_orientation_hint(detections):
    vertical = 0
    horizontal = 0

    for det in detections:
        if "bbox" not in det:
            continue

        x1, y1, x2, y2 = det["bbox"]
        w = max(1, x2 - x1)
        h = max(1, y2 - y1)

        if h / w > 1.25:
            vertical += 1
        elif h / w < 0.8:
            horizontal += 1

    if vertical > horizontal:
        return "mostly vertical arrangement"
    if horizontal > vertical:
        return "mostly horizontal arrangement"

    return ""


# -------------------------------
# Art Target Suggestion (Hybrid)
# -------------------------------

def suggest_art_target(material_counts):

    mats = set(material_counts.keys())

    if "bottle" in mats:
        return "lamp sculpture"

    if "cup" in mats:
        return "flower sculpture"

    if "can" in mats or "tin" in mats:
        return "abstract metal sculpture"

    if "paper" in mats or "cardboard" in mats:
        return "wall decor artwork"

    return "recycled sculpture"


# -------------------------------
# Prompt Builder
# -------------------------------

def build_prompt(

    detections,
    biodegradable_count,
    non_biodegradable_count,
    style=None,
    mood=None,
    user_notes=None,
    art_target_override=None
):
    print(">>> NEW PROMPT BUILDER ACTIVE <<<")

    # -------------------------------
    # Collect recyclable objects
    # -------------------------------
    materials = [
        det["class"]
        for det in detections
        if det.get("biodeg_label") == "Non-Biodegradable"
    ]

    if not materials:
        raise ValueError("No recyclable materials found")

    counts = Counter(materials)
    total_objects = sum(counts.values())

    # -------------------------------
    # Hybrid art target
    # -------------------------------
    suggested_target = suggest_art_target(counts)
    final_target = art_target_override if art_target_override else suggested_target

    # -------------------------------
    # Material phrase
    # -------------------------------
    material_parts = []
    for mat, count in counts.items():
        if count == 1:
            material_parts.append(f"a {mat}")
        else:
            material_parts.append(f"{count} {mat}s")

    materials_text = ", ".join(material_parts)

    # -------------------------------
    # Composition
    # -------------------------------
    composition_text = choose_composition(total_objects)

    # -------------------------------
    # Shape + texture grounding
    # -------------------------------
    orientation_hint = extract_orientation_hint(detections)

    shape_hints = [
        OBJECT_SHAPE_MAP[m]
        for m in counts.keys()
        if m in OBJECT_SHAPE_MAP
    ]

    texture_hints = [
        MATERIAL_TEXTURE_MAP[m]
        for m in counts.keys()
        if m in MATERIAL_TEXTURE_MAP
    ]

    shape_text = ", ".join(shape_hints)
    texture_text = ", ".join(texture_hints)

    # -------------------------------
    # Lamp-specific glow (functional realism)
    # -------------------------------
    lamp_glow_hint = ""
    if "lamp" in final_target.lower():
        lamp_glow_hint = "soft warm internal light glow"

    # -------------------------------
    # Base prompt (CLEAN + IMPRESSIVE)
    # -------------------------------
    base_prompt = (
        f"A recycled {final_target} created from {materials_text}, "
        f"{composition_text}, "
        f"{orientation_hint}, "
        f"{shape_text}, "
        f"{texture_text}, "
        f"{lamp_glow_hint}, "
        f"visibly handcrafted structure, carefully assembled recycled components, "
        f"realistic material behavior, believable physical construction, "
        f"artistic handcrafted recycled design"
    )

    # -------------------------------
    # Style & Mood
    # -------------------------------
    STYLE_MAP = {
        "minimal": "minimalist style",
        "abstract": "abstract artistic interpretation",
        "modern": "modern contemporary design",
        "handcrafted": "handcrafted aesthetic"
    }

    MOOD_MAP = {
        "calm": "soft lighting",
        "hopeful": "uplifting mood",
        "earthy": "earthy natural tones",
        "dramatic": "dramatic lighting"
    }

    style_text = STYLE_MAP.get(style, "")
    mood_text = MOOD_MAP.get(mood, "")
    user_hint = sanitize_user_text(user_notes)

    # -------------------------------
    # Final Prompt
    # -------------------------------
    final_prompt = ", ".join(
        p for p in [
            base_prompt,
            style_text,
            mood_text,
            user_hint,
            "high detail, clean composition, professional artwork, visibly transformed into recycled art, not a photograph"
        ] if p
    )

    # -------------------------------
    # Negative Prompt
    # -------------------------------
    negative_prompt = (
        "people, faces, animals, realistic photo, unchanged object, messy composition, "
        "low quality, blurry, distorted, watermark, text"
    )

    return final_prompt, negative_prompt
