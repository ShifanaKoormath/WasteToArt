def create_prompt(material, description):
    base = {
        "Biodegradable": "natural earthy recycled crafts, warm organic textures",
        "Non-Biodegradable": "upcycled plastic art, modern reuse, sustainability"
    }

    final_prompt = (
        f"Creative upcycled {material.lower()} material turned into unique art. "
        f"{base.get(material, '')}. "
        f"{description}"
    )

    return final_prompt
