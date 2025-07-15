import os
from rembg import remove
from PIL import Image

INPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\portable_blender_filtered"
OUTPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\portable_blender_nobg"

os.makedirs(OUTPUT_DIR, exist_ok=True)

for file_name in os.listdir(INPUT_DIR):
    if file_name.endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(INPUT_DIR, file_name)
        output_path = os.path.join(OUTPUT_DIR, file_name)

        with Image.open(input_path) as img:
            result = remove(img)
            result.save(output_path)

        print(f"🧼 Removed background: {file_name}")
