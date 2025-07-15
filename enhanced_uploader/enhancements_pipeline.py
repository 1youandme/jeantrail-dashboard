# ✅ المسار: C:\Users\dell\JeanTrail_AI\enhanced_uploader\enhancements_pipeline.py

import os
import json
import sys
import requests
from PIL import Image
from io import BytesIO
from rembg import remove
import pytesseract
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed

# ✅ تحميل متغيرات البيئة
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "product-images"

# ✅ المسارات
BASE_DIR = os.path.dirname(__file__)
BLOGGER_RESULTS = os.path.join(BASE_DIR, "..", "blogger", "blogger_trending_results.json")
LOGO_PATH = os.path.join(BASE_DIR, "..", "logo.png")
UPLOADED_FILE = os.path.join(BASE_DIR, "uploaded_bloggers.json")
PROGRESS_FILE = os.path.join(BASE_DIR, "last_processed_bloggers.txt")

# ✅ تحميل اللوجو
logo = Image.open(LOGO_PATH).convert("RGBA").resize((80, 80))

# ✅ إعدادات الدُفعات
BATCH_SIZE = 25

# ✅ التحقق من الجودة (أقل من 300x300 تعتبر ضعيفة)
def is_high_quality(image):
    return image.width >= 300 and image.height >= 300

def contains_chinese(image):
    text = pytesseract.image_to_string(image, lang="eng+chi_sim")
    return any('\u4e00' <= char <= '\u9fff' for char in text)

@retry(stop=stop_after_attempt(5), wait=wait_fixed(5))
def download_image(url):
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGBA")

@retry(stop=stop_after_attempt(3), wait=wait_fixed(3))
def upload_image_to_supabase(image_bytes, filename):
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{filename}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "image/png"
    }
    response = requests.put(url, headers=headers, data=image_bytes)
    response.raise_for_status()
    return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{filename}"

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
        print("✅ Uploaded:", product['title'])
    else:
        print("❌ Upload failed:", response.text)

def generate_description(original_desc):
    # ⚠️ محاكاة توليد وصف ذكي — يتم لاحقًا استبداله بـ AI فعليًا
    return f"{original_desc.strip()[:100]}... Discover more in JeanTrail's trending collection!"

# ✅ تحميل المنتجات من ملف البلوجرز
with open(BLOGGER_RESULTS, 'r', encoding='utf-8') as f:
    all_products = json.load(f)

# ✅ تحميل المنتجات المرفوعة سابقًا
uploaded_ids = set()
if os.path.exists(UPLOADED_FILE):
    with open(UPLOADED_FILE, 'r', encoding='utf-8') as f:
        uploaded_ids = set(json.load(f))

# ✅ متابعة التقدم
start_from = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r') as f:
        start_from = int(f.read().strip())

end_at = min(start_from + BATCH_SIZE, len(all_products))

for idx, product in enumerate(all_products[start_from:end_at], start=start_from):
    product_id = product.get("source_url")
    if product_id in uploaded_ids:
        print(f"⏭️ Already uploaded: {product_id}")
        continue

    # محاكاة صور مرتبطة بالمنتج — يجب توفير صور حقيقية لاحقًا
    image_list = [
        f"https://dummyimage.com/400x400/000/fff&text={product['product_name'].replace(' ', '+')}"
    ]

    gallery_urls = []
    for img_idx, image_url in enumerate(image_list):
        try:
            original = download_image(image_url)

            if not is_high_quality(original) or contains_chinese(original):
                print(f"⚠️ Skipping low-quality or Chinese image")
                continue

            nobg = remove(original)
            final_img = Image.alpha_composite(nobg, Image.new("RGBA", nobg.size))
            final_img.paste(logo, (10, 10), logo)
            buffer = BytesIO()
            final_img.save(buffer, format="PNG")
            buffer.seek(0)
            filename = f"blogger_{idx+1}_img_{img_idx+1}.png"
            uploaded_url = upload_image_to_supabase(buffer.getvalue(), filename)
            gallery_urls.append(uploaded_url)

        except Exception as e:
            print(f"❌ Image error: {e}")

    if not gallery_urls:
        print(f"⛔ Skipping product {idx+1}: No valid images")
        continue

    product_payload = {
        "title": product['product_name'],
        "description": generate_description(product['product_name']),
        "price": 49.99,
        "image": gallery_urls[0],
        "gallery": gallery_urls
    }

    upload_product_to_supabase(product_payload)

    # ✅ تحديث السجلات
    uploaded_ids.add(product_id)
    with open(UPLOADED_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(uploaded_ids), f, ensure_ascii=False, indent=2)

    with open(PROGRESS_FILE, 'w') as f:
        f.write(str(idx + 1))

    print(f"✅ Finished product {idx+1}/{end_at}")

    if idx + 1 >= end_at:
        print("🛑 Batch complete — will auto-restart via GitHub Actions.")
        sys.exit(99)

print("🎉 All blogger products processed.")
if os.path.exists(PROGRESS_FILE):
    os.remove(PROGRESS_FILE)
