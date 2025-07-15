# ✅ الملف: process_from_urls.py
# 📁 المسار: C:\Users\dell\JeanTrail_AI\scripts\alibaba\process_from_urls.py

import os
import json
import requests
from PIL import Image
from rembg import remove
from io import BytesIO
import pytesseract

# إعدادات المسارات
KEYWORD = "portable_blender"
BASE_PATH = f"C:/Users/dell/JeanTrail_AI"
INPUT_JSON = f"{BASE_PATH}/scripts/results/{KEYWORD}.json"
FILTERED_JSON = f"{BASE_PATH}/scripts/results/{KEYWORD}_filtered.json"
LOGO_PATH = f"{BASE_PATH}/jeantrail_frontend/public/logo.png"

# المجلدات للصور
FILTERED_DIR = f"{BASE_PATH}/images/{KEYWORD}_filtered"
FINAL_DIR = f"{BASE_PATH}/images/{KEYWORD}_final"
os.makedirs(FILTERED_DIR, exist_ok=True)
os.makedirs(FINAL_DIR, exist_ok=True)

# تحميل صورة من رابط
def download_image(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except:
        return None

# كشف النصوص في الصورة
def has_text(image):
    text = pytesseract.image_to_string(image)
    return bool(text.strip())

# وضع اللوجو
def add_logo(image, logo_path):
    try:
        logo = Image.open(logo_path).convert("RGBA")
        logo = logo.resize((80, 80))  # تغيير الحجم حسب الحاجة

        image = image.convert("RGBA")
        image.paste(logo, (10, 10), logo)
        return image
    except:
        return image

# المعالجة
with open(INPUT_JSON, "r", encoding="utf-8") as f:
    products = json.load(f)

filtered_products = []

for product in products:
    valid_images = []
    image_urls = product.get("images", [])
    for img_url in image_urls:
        img = download_image(img_url)
        if not img:
            continue

        # تصغير وتحويل لاختبار النص
        small = img.resize((300, 300))
        if has_text(small):
            continue

        filename = os.path.basename(img_url).split("?")[0]
        raw_path = os.path.join(FILTERED_DIR, filename)

        # إزالة الخلفية
        try:
            no_bg = remove(img.convert("RGBA"))
        except:
            no_bg = img.convert("RGBA")

        # إضافة اللوجو
        final = add_logo(no_bg, LOGO_PATH)
        final.save(os.path.join(FINAL_DIR, filename))
        valid_images.append(filename)

    if valid_images:
        product["valid_images"] = valid_images
        filtered_products.append(product)

with open(FILTERED_JSON, "w", encoding="utf-8") as f:
    json.dump(filtered_products, f, indent=2, ensure_ascii=False)

print(f"✅ تمت فلترة {len(filtered_products)} منتج (من أصل {len(products)})")
print(f"📁 تم حفظ النتائج في: {FILTERED_JSON}")
