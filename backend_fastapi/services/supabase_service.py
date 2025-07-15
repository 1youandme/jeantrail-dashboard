import os
import requests
from dotenv import load_dotenv

# تحميل ملف البيئة
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
TABLE = "products"

# طباعة للتأكد
print("✅ SUPABASE_URL:", SUPABASE_URL)
print("✅ SUPABASE_KEY:", SUPABASE_KEY[:10] + "...")

def get_products_from_supabase():
    print("✅ SUPABASE_URL LOADED:", SUPABASE_URL)
    print("✅ SUPABASE_KEY LOADED:", SUPABASE_KEY[:10] + "...")

    url = f"{SUPABASE_URL}/rest/v1/products?select=*"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }

    res = requests.get(url, headers=headers)
    print("🔎 Response from Supabase:", res.text)  # أضف هذا السطر
    return res.json()

def insert_product(data: dict):
    try:
        url = f"{SUPABASE_URL}/rest/v1/{TABLE}"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        res = requests.post(url, headers=headers, json=data)
        return {"status": "success", "data": res.json()} if res.status_code in [200, 201] else {"status": "error", "message": res.text}
    except Exception as e:
        return {"status": "error", "message": str(e)}
