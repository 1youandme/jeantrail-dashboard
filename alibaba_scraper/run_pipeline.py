import os
import json
import requests
from PIL import Image
from io import BytesIO
from rembg import remove
import pytesseract
from dotenv import load_dotenv

# ✅ تحميل متغيرات البيئة
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "product-images"

# ✅ إعداد المسارات
BASE_DIR = os.path.dirname(__file__)
PRODUCTS_JSON = os.path.join(BASE_DIR, "scripts", "results", "portable_blender.json")
LOGO_PATH = os.path.join(BASE_DIR, "jeantrail_frontend", "public", "logo.png")

# ✅ تحميل اللوجو
logo = Image.open(LOGO_PATH).convert("RGBA").resize((80, 80))

def contains_chinese(image):
    text = pytesseract.image_to_string(image, lang="eng+chi_sim")
    return any('\u4e00' <= char <= '\u9fff' for char in text)

def upload_image_to_supabase(image_bytes, filename):
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "image/png"
    }
    response = requests.put(url, headers=headers, data=image_bytes)
    if response.status_code in [200, 201]:
        public_url = f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"
        return public_url
    else:
        print("❌ Image upload failed:", response.text)
        return None

def upload_product_to_supabase(product):
    url = f"{SUPABASE_URL}/rest/v1/products"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    response = requests.post(url, headers=headers, json=product)
    if response.status_code in [200, 201]:
        print("✅ Product uploaded:", product['title'])
    else:
        print("❌ Product upload failed:", response.text)

with open(PRODUCTS_JSON, 'r', encoding='utf-8') as f:
    products = json.load(f)

for idx, product in enumerate(products):
    title = product.get("title") or product.get("name") or f"Product {idx+1}"
    image_list = product.get("images", [])
    price = float(product.get("price") or 49.99)
    description = product.get("description", "Smart product from JeanTrail.")
    
    gallery_urls = []
    chinese_count = 0
    processed_count = 0

    for img_idx, image_url in enumerate(image_list):
        try:
            print(f"🖼️ Processing image {img_idx+1}/{len(image_list)} for product {idx+1}")
            img_response = requests.get(image_url, timeout=20)
            original = Image.open(BytesIO(img_response.content)).convert("RGBA")

            if contains_chinese(original):
                chinese_count += 1
                continue

            # إزالة الخلفية
            nobg = remove(original)

            # دمج اللوجو
            final_img = Image.alpha_composite(nobg, Image.new("RGBA", nobg.size))
            final_img.paste(logo, (10, 10), logo)

            # حفظ مؤقت
            buffer = BytesIO()
            final_img.save(buffer, format="PNG")
            buffer.seek(0)

            filename = f"product_{idx+1}_img_{img_idx+1}.png"
            image_url = upload_image_to_supabase(buffer.getvalue(), filename)

            if image_url:
                gallery_urls.append(image_url)
                processed_count += 1

        except Exception as e:
            print(f"❌ Failed to process image {img_idx+1}: {e}")

    # لو تم تجاهل كل الصور بسبب الصينية، اسمح بواحدة على الأقل
    if processed_count == 0 and chinese_count == len(image_list):
        print("⚠️ All images contain Chinese, fallback to first image.")
        try:
            img_response = requests.get(image_list[0], timeout=10)
            original = Image.open(BytesIO(img_response.content)).convert("RGBA")
            nobg = remove(original)
            final_img = Image.alpha_composite(nobg, Image.new("RGBA", nobg.size))
            final_img.paste(logo, (10, 10), logo)
            buffer = BytesIO()
            final_img.save(buffer, format="PNG")
            buffer.seek(0)
            filename = f"product_{idx+1}_fallback.png"
            image_url = upload_image_to_supabase(buffer.getvalue(), filename)
            if image_url:
                gallery_urls.append(image_url)
        except Exception as e:
            print("❌ Fallback image failed:", e)

    if not gallery_urls:
        print(f"⛔ Skipping product {idx+1} – No valid images")
        continue

    product_payload = {
        "title": title,
        "description": description,
        "price": price,
        "image": gallery_urls[0],   # الصورة الرئيسية
        "gallery": gallery_urls     # كل الصور الأخرى
    }

    upload_product_to_supabase(product_payload)
