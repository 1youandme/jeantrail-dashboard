# ✅ الملف: process_images_from_urls.py
# 📁 المسار: C:\Users\dell\JeanTrail_AI\scripts\alibaba

import requests
from PIL import Image, ImageDraw
from io import BytesIO
import os
import json

from rembg import remove

# المسارات
RESULTS_JSON = r"C:\Users\dell\JeanTrail_AI\scripts\results\portable_blender_filtered.json"
OUTPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\portable_blender_final"
LOGO_PATH = r"C:\Users\dell\JeanTrail_AI\jeantrail_frontend\public\logo.png"

# تأكد من وجود المجلد النهائي
os.makedirs(OUTPUT_DIR, exist_ok=True)

# تحميل لوجو JeanTrail
logo = Image.open(LOGO_PATH).convert("RGBA")
logo = logo.resize((100, 100))  # حجم مناسب

# تحميل المنتجات
with open(RESULTS_JSON, "r", encoding="utf-8") as f:
    products = json.load(f)

saved = 0

for product in products:
    try:
        url = product["image_url"]
        response = requests.get(url, timeout=10)
        img = Image.open(BytesIO(response.content)).convert("RGBA")

        # إزالة الخلفية
        img_nobg = remove(img)

        # لصق اللوجو في الزاوية العلوية اليسرى
        img_nobg.paste(logo, (10, 10), logo)

        # حفظ الصورة النهائية بنفس اسم المنتج
        filename = os.path.basename(url).split("?")[0]
        output_path = os.path.join(OUTPUT_DIR, filename)
        img_nobg.save(output_path)

        saved += 1
        print(f"✅ Saved: {filename}")

    except Exception as e:
        print(f"❌ Failed to process {product.get('name', 'Unknown')}: {e}")

print(f"\n🎉 تم إنشاء {saved} صورة بنجاح داخل {OUTPUT_DIR}")
