import sys, os, uuid
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detection.detect import run_detection
from classification.classify import predict_class
from generation.generate_art import generate_art


def process_image(input_image, return_path=False):
    print("\n🔍 Running YOLO Detection...")
    crop_paths = run_detection(input_image)

    print(f"\nDetected {len(crop_paths)} object crops:")
    for c in crop_paths:
        print(" -", c)

    print("\n🧪 Running Classification...")
    class_results = []
    for c in crop_paths:
        predicted_class = predict_class(c)
        class_results.append(predicted_class)

    biodegradable_count = class_results.count("Biodegradable")
    non_biodegradable_count = class_results.count("Non-Biodegradable")

    print("\n📊 Summary:")
    print(f"Biodegradable: {biodegradable_count}")
    print(f"Non-Biodegradable: {non_biodegradable_count}")

    print("\n📝 Generating Prompt...")

    prompt_text = (
        f"Creative upcycled art made from "
        f"{non_biodegradable_count} non-biodegradable and "
        f"{biodegradable_count} biodegradable materials. "
        f"Eco-friendly aesthetic, handcrafted recycled artwork."
    )

    print("Generated Prompt:", prompt_text)

    print("\n🎨 Generating ART via Local Stable Diffusion...")

    # Absolute output directory
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # → backend/
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")           # → backend/output
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, f"{uuid.uuid4().hex}.png")

    generate_art(prompt_text, output_path)

    print("\n✅ DONE! Saved final image as:", output_path)

    if return_path:
        return output_path  # ALWAYS absolute path


if __name__ == "__main__":
    test_image = "Plastic bottles.jpg"
    process_image(test_image)
