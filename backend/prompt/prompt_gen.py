from backend.embedding.embed import get_text_embedding
import numpy as np

STYLE_TEMPLATES = [
    "highly detailed eco-art sculpture made from recycled materials",
    "creative upcycled artwork with artistic transformation of waste",
    "modern environmental art built from discarded objects",
    "handcrafted recycled art installation with intricate details",
    "eco-friendly conceptual artwork emphasizing sustainability"
]

NEGATIVE_PROMPT = (
    "blurry, low quality, distorted, deformed hands, incorrect anatomy, "
    "text, watermark, logo, noisy background, artificial colors, extra limbs, bad composition"
)

def create_prompt(detections, bio_count, nonbio_count):
    # Extract UNIQUE objects only
    unique_objects = sorted(list({det["class"] for det in detections}))
    object_list = ", ".join(unique_objects)

    # Build base description
    material_description = (
        f"Artwork created using discarded {object_list}. "
        f"These waste items are creatively transformed into artistic forms. "
    )

    # SBERT selects best style template
    embeddings = [get_text_embedding(t) for t in STYLE_TEMPLATES]
    base_vector = get_text_embedding(material_description)

    similarities = [np.dot(base_vector, e) for e in embeddings]
    best_style = STYLE_TEMPLATES[int(np.argmax(similarities))]

    # FINAL prompt
    final_prompt = (
        f"{material_description}"
        f"{best_style}. "
        f"Biodegradable items: {bio_count}, Non-biodegradable items: {nonbio_count}. "
        "Highly aesthetic, clean composition, cinematic lighting, artistic presentation."
    )

    return final_prompt, NEGATIVE_PROMPT
