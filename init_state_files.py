import os
import json

BASE_DIR = os.path.abspath(".")
progress_file = os.path.join(BASE_DIR, "last_processed.txt")
uploaded_file = os.path.join(BASE_DIR, "uploaded_products.json")
blogger_result_file = os.path.join(BASE_DIR, "blogger", "blogger_trending_results.json")

# 📝 last_processed.txt
if not os.path.exists(progress_file):
    with open(progress_file, "w", encoding="utf-8") as f:
        f.write("0")
    print("✅ Created last_processed.txt")

# 📝 uploaded_products.json
if not os.path.exists(uploaded_file):
    with open(uploaded_file, "w", encoding="utf-8") as f:
        json.dump([], f)
    print("✅ Created uploaded_products.json")

# 📝 blogger_trending_results.json
os.makedirs(os.path.join(BASE_DIR, "blogger"), exist_ok=True)
if not os.path.exists(blogger_result_file):
    with open(blogger_result_file, "w", encoding="utf-8") as f:
        json.dump([], f)
    print("✅ Created blogger_trending_results.json")
