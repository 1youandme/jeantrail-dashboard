import os
import json
from datetime import datetime

# ✅ المسارات
BASE_DIR = os.path.dirname(__file__)
BLOGGERS_FILE = os.path.join(BASE_DIR, 'blogger_trending.json')
RESULTS_FILE = os.path.join(BASE_DIR, 'blogger_trending_results.json')

# ✅ تحميل قائمة البلوجرز حسب المنصة
with open(BLOGGERS_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

results = []

for platform, bloggers in data.items():
    for blogger in bloggers:
        name = blogger.get("name")
        username = blogger.get("username")
        followers = blogger.get("followers")

        profile_url = ""
        if platform == "tiktok":
            profile_url = f"https://www.tiktok.com/@{username}"
        elif platform == "instagram":
            profile_url = f"https://www.instagram.com/{username}"

        # 🧠 محاكاة استخراج منتج شائع لكل بلوجر (لاحقًا سيتم ربطه بمصادر حقيقية)
        simulated_product = {
            "blogger": name,
            "platform": platform,
            "followers": followers,
            "product_name": f"Trending product by {name}",
            "source_url": profile_url,
            "detected_at": datetime.utcnow().isoformat()
        }

        results.append(simulated_product)

# ✅ حفظ النتائج في ملف واحد
with open(RESULTS_FILE, 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"✅ Saved {len(results)} trending products to {RESULTS_FILE}")
