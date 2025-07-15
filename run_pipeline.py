import os
import json
import sys
import glob
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

# ✅ إعداد المسارات
BASE_DIR = os.path.dirname(__file__)
RESULTS_DIR = os.path.join(BASE_DIR, "products", "results")
LOGO_PATH = os.path.join(BASE_DIR, "logo.png")
PROGRESS_FILE = os.path.join(BASE_DIR, "last_processed.txt")
UPLOADED_FILE = os.path.join(BASE_DIR, "uploaded_products.json")

# ✅ إعدادات الدُفعات
BATCH_SIZE = 50
logo = Image.open(LOGO_PATH).convert("RGBA").resize((80, 80))

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
        print("✅ Product uploaded:", product['title'])
    else:
        print("❌ Product upload failed:", response.text)

# ✅ تحميل المنتجات التي تم رفعها سابقًا
uploaded_ids = set()
if os.path.exists(UPLOADED_FILE):
    with open(UPLOADED_FILE, 'r', encoding='utf-8') as f:
        uploaded_ids = set(json.load(f))

# ✅ استكمال من آخر نقطة
start_file = None
start_index = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r') as f:
        state = json.load(f)
        start_file = state.get("file")
        start_index = state.get("index", 0)

json_files = sorted(glob.glob(os.path.join(RESULTS_DIR, "*.json")))
resume_found = start_file is None

for json_path in json_files:
    file_name = os.path.basename(json_path)

    # تخطي الملفات حتى نصل لملف الاستكمال
    if not resume_found:
        if file_name == start_file:
            resume_found = True
        else:
            continue

    with open(json_path, 'r', encoding='utf-8') as f:
        products = json.load(f)

    end_at = min(start_index + BATCH_SIZE, len(products))
    print(f"\n🛠️ Processing file: {file_name} from index {start_index} to {end_at - 1}")

    for idx, product in enumerate(products[start_index:end_at], start=start_index):
        product_id = product.get("url") or product.get("name")
        if product_id in uploaded_ids:
            print(f"⏭️ Skipping (already uploaded): {product_id}")
            continue

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
                original = download_image(image_url)

                if contains_chinese(original):
                    chinese_count += 1
                    continue

                nobg = remove(original)
                final_img = Image.alpha_composite(nobg, Image.new("RGBA", nobg.size))
                final_img.paste(logo, (10, 10), logo)
                buffer = BytesIO()
                final_img.save(buffer, format="PNG")
                buffer.seek(0)
                filename = f"{file_name}__{idx+1}_img_{img_idx+1}.png"
                image_url = upload_image_to_supabase(buffer.getvalue(), filename)
                gallery_urls.append(image_url)
                processed_count += 1

            except Exception as e:
                print(f"❌ Failed to process image {img_idx+1}: {e}")

        if processed_count == 0 and chinese_count == len(image_list):
            print("⚠️ All images contain Chinese, fallback to first image.")
            try:
                original = download_image(image_list[0])
                nobg = remove(original)
                final_img = Image.alpha_composite(nobg, Image.new("RGBA", nobg.size))
                final_img.paste(logo, (10, 10), logo)
                buffer = BytesIO()
                final_img.save(buffer, format="PNG")
                buffer.seek(0)
                filename = f"{file_name}__{idx+1}_fallback.png"
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
            "image": gallery_urls[0],
            "gallery": gallery_urls
        }

        upload_product_to_supabase(product_payload)

        uploaded_ids.add(product_id)

        # 📝 حفظ التقدم
        with open(PROGRESS_FILE, 'w') as f:
            json.dump({"file": file_name, "index": idx + 1}, f)

        with open(UPLOADED_FILE, 'w', encoding='utf-8') as f:
            json.dump(list(uploaded_ids), f, ensure_ascii=False, indent=2)

        if idx + 1 >= end_at:
            print(f"🛑 Batch {BATCH_SIZE} complete. Halting for restart...")
            sys.exit(99)

    start_index = 0  # ابدأ من أول منتج في الملف التالي

print("🎉 All products from all files processed.")
if os.path.exists(PROGRESS_FILE):
    os.remove(PROGRESS_FILE)
