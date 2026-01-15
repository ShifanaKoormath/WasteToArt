import requests
import base64

def generate_art(prompt, negative_prompt, output_path):
    print("Sending prompt to Stable Diffusion...")

    payload = {
        "prompt": prompt,
        "negative_prompt": negative_prompt,
        "steps": 28,               # better quality than 20
        "cfg_scale": 8.0,          # good balance of creativity vs accuracy
        "sampler_name": "Euler a", # stable and sharp
        "width": 512,
        "height": 512,
        "seed": -1,                # random seed for variety
    }

    response = requests.post(
        "http://127.0.0.1:7860/sdapi/v1/txt2img",
        json=payload
    )

    if response.status_code != 200:
        raise RuntimeError(f"SD Error {response.status_code}: {response.text}")

    # Extract base64 image
    img_data = response.json()["images"][0]
    img_bytes = base64.b64decode(img_data.split(",", 1)[0])

    # Save to file
    with open(output_path, "wb") as f:
        f.write(img_bytes)

    print("Image saved as:", output_path)
    return output_path