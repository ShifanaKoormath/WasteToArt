import sys, os, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detection.detect import run_detection
from classification.classify import predict_class
from prompt.prompt_gen import create_prompt
from generation.generate_art import generate_art


def process_image(input_image, return_path=False):
    print("\n🔍 Running YOLO Detection...")

    detections = run_detection(input_image)

    print(f"\nDetected {len(detections)} object(s):")
    for det in detections:
        print(f" - {det['class']} (conf {det['conf']:.2f}) → {det['crop_path']}")

    if len(detections) == 0:
        return {
            "error": "NO_OBJECTS",
            "message": "No detectable waste objects found in the image."
        }

    print("\n🧪 Running Classification...")

    biodegradable_count = 0
    non_biodegradable_count = 0

    for det in detections:
        label = predict_class(det["crop_path"])
        det["biodeg_label"] = label

        if label == "Biodegradable":
            biodegradable_count += 1
        else:
            non_biodegradable_count += 1

    print("\n📊 Summary:")
    print(f"Biodegradable: {biodegradable_count}")
    print(f"Non-Biodegradable: {non_biodegradable_count}")

    # ---------------------------------------------------------
    # 🚫 STOP if no non-biodegradable objects are present
    # ---------------------------------------------------------
    if non_biodegradable_count == 0:
        print("\n⚠️ Only biodegradable objects detected. No artwork required.")
        return {
            "error": "NO_RECYCLABLES",
            "message": "Only biodegradable objects detected. No artwork will be generated."
        }

    print("\n📝 Generating Prompt with SBERT...")

    prompt_text, negative_prompt = create_prompt(
        detections,
        biodegradable_count,
        non_biodegradable_count
    )

    print("\nGenerated Prompt:")
    print(prompt_text)

    print("\nNegative Prompt:")
    print(negative_prompt)

    print("\n🎨 Generating ART via Local Stable Diffusion...")

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}.png")

    generate_art(prompt_text, negative_prompt, output_path)

    print("\n✅ DONE! Final image saved as:", output_path)

    # If frontend expects only path string
    if return_path:
        return output_path

    return output_path
