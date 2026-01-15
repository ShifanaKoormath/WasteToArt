# backend/prompt/prompt_builder.py
import re

# -------------------------------
# Guardrails
# -------------------------------

FORBIDDEN_KEYWORDS = [
    "human", "person", "face", "animal", "dragon", "monster",
    "weapon", "gun", "blood", "war", "car", "bike", "building",
    "gold", "diamond", "space", "galaxy"
]

MAX_USER_TEXT_LEN = 150


def sanitize_user_text(text: str) -> str:
    if not text:
        return ""

    text = text.lower().strip()
    text = text[:MAX_USER_TEXT_LEN]

    for word in FORBIDDEN_KEYWORDS:
        text = re.sub(rf"\b{word}\b", "", text)

    return text.strip()


# -------------------------------
# Prompt Builder
# -------------------------------

def build_prompt(
    detections,
    biodegradable_count,
    non_biodegradable_count,
    style=None,
    mood=None,
    user_notes=None
):
    """
    This function is the ONLY place where final prompts are built.
    Frontend input is treated as suggestions, not authority.
    """

    # ---- Extract non-biodegradable objects only ----
    materials = []
    for det in detections:
        if det.get("biodeg_label") == "Non-Biodegradable":
            materials.append(det["class"])

    materials = list(set(materials))

    if not materials:
        raise ValueError("No recyclable materials available for prompt generation")

    # ---- System-controlled base prompt ----
    base_prompt = (
        f"A recycled art sculpture made from discarded {', '.join(materials)}, "
        f"eco-friendly upcycled artwork, sustainable materials, environmental theme"
    )

    # ---- Style presets (safe) ----
    STYLE_MAP = {
        "minimal": "minimalist design, clean forms",
        "abstract": "abstract artistic form",
        "modern": "modern contemporary sculpture",
        "handcrafted": "handcrafted recycled art look"
    }

    MOOD_MAP = {
        "calm": "soft lighting, calm atmosphere",
        "hopeful": "hopeful and positive mood",
        "earthy": "natural earthy tones",
        "dramatic": "dramatic lighting and contrast"
    }

    style_text = STYLE_MAP.get(style, "")
    mood_text = MOOD_MAP.get(mood, "")
    user_text = sanitize_user_text(user_notes)

    # ---- Final prompt assembly ----
    final_prompt = ", ".join(
        part for part in [
            base_prompt,
            style_text,
            mood_text,
            user_text,
            "studio lighting, high quality, detailed"
        ] if part
    )

    # ---- Negative prompt (fixed) ----
    negative_prompt = (
        "real people, faces, animals, fantasy creatures, weapons, "
        "text, watermark, low quality, blurry, distorted"
    )

    return final_prompt, negative_prompt
