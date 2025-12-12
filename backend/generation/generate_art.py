import requests
import base64

def generate_art(prompt, output_path):
    print("Sending prompt to Stable Diffusion...")

    payload = {
        "prompt": prompt,
        "steps": 20,
        "width": 512,
        "height": 512
    }

    response = requests.post("http://127.0.0.1:7860/sdapi/v1/txt2img", json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Error {response.status_code}: {response.text}")

    img_data = response.json()["images"][0]
    img_bytes = base64.b64decode(img_data.split(",", 1)[0])

    with open(output_path, "wb") as f:
        f.write(img_bytes)

    print("Image saved as:", output_path)
    return output_path
