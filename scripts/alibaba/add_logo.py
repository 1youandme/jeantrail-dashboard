import os
from PIL import Image

LOGO_PATH = r"C:\Users\dell\JeanTrail_AI\jeantrail_frontend\public\logo.png"
INPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\portable_blender_nobg"
OUTPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\portable_blender_final"

os.makedirs(OUTPUT_DIR, exist_ok=True)
logo = Image.open(LOGO_PATH).convert("RGBA")
logo = logo.resize((80, 80))  # حجم اللوجو النهائي

for filename in os.listdir(INPUT_DIR):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        product_path = os.path.join(INPUT_DIR, filename)
        output_path = os.path.join(OUTPUT_DIR, filename)

        with Image.open(product_path).convert("RGBA") as base:
            base.paste(logo, (10, 10), logo)
            base.save(output_path)

        print(f"✅ Logo added to: {filename}")
