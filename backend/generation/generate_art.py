import requests
import base64
import cv2


SD_URL = "http://127.0.0.1:7860"


# --------------------------------------------------
# Encode image to base64 (for img2img)
# --------------------------------------------------
def encode_image_to_base64(path):
    img = cv2.imread(path)
    if img is None:
        raise RuntimeError("Failed to read input image for img2img")

    _, buffer = cv2.imencode(".png", img)
    return base64.b64encode(buffer).decode("utf-8")


# --------------------------------------------------
# Main generation function
# --------------------------------------------------
def generate_art(prompt, negative_prompt, output_path, input_image=None):

    try:
        # ==========================================================
        # MODE 1 — IMG2IMG (Preserve shape + transform into art)
        # ==========================================================
        if input_image is not None:
            print("Sending IMG2IMG request to Stable Diffusion...")

            img_b64 = encode_image_to_base64(input_image)

            payload = {
                "init_images": [img_b64],
                "prompt": prompt,
                "negative_prompt": (
                    negative_prompt
                    + ", original background, realistic photo, unchanged object, duplicate image"
                ),

                # Transformation strength (KEY)
                "denoising_strength": 0.65,

                "steps": 32,
                "cfg_scale": 5.8,
                "sampler_name": "DPM++ 2M Karras",

                "width": 512,
                "height": 512,
                "seed": -1,

                # High resolution pass
                "enable_hr": True,
                "hr_scale": 1.8,
                "hr_upscaler": "Latent",
                "hr_second_pass_steps": 16,
            }

            response = requests.post(
                f"{SD_URL}/sdapi/v1/img2img",
                json=payload,
                timeout=180
            )

        # ==========================================================
        # MODE 2 — TXT2IMG (Fallback)
        # ==========================================================
        else:
            print("Sending TXT2IMG request to Stable Diffusion...")

            payload = {
                "prompt": prompt,
                "negative_prompt": negative_prompt,

                "steps": 30,
                "cfg_scale": 7.0,
                "sampler_name": "DPM++ 2M Karras",

                "width": 512,
                "height": 512,
                "seed": -1,

                "enable_hr": True,
                "hr_scale": 1.8,
                "hr_upscaler": "Latent",
                "hr_second_pass_steps": 18,
            }

            response = requests.post(
                f"{SD_URL}/sdapi/v1/txt2img",
                json=payload,
                timeout=180
            )

        # ==========================================================
        # Handle response
        # ==========================================================
        if response.status_code != 200:
            raise RuntimeError(f"SD Error {response.status_code}: {response.text}")

        img_data = response.json()["images"][0]
        img_bytes = base64.b64decode(img_data.split(",", 1)[0])

        with open(output_path, "wb") as f:
            f.write(img_bytes)

        print("Image saved:", output_path)
        return output_path

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Stable Diffusion not running")

    except Exception as e:
        raise RuntimeError(f"Generation failed: {str(e)}")
