import os
import shutil

# المسار الأساسي للمشروع
base_dir = os.path.abspath(os.path.dirname(__file__))

# المسارات
source_paths = [
    "run_pipeline.py",
    "scripts/results/portable_blender.json",
    "jeantrail_frontend/public/logo.png"
]

destination_dir = os.path.join(base_dir, "alibaba_scraper")

# إنشاء المجلد لو مش موجود (تحسّبي فقط)
os.makedirs(destination_dir, exist_ok=True)

for path in source_paths:
    src = os.path.join(base_dir, path)
    if os.path.exists(src):
        dst = os.path.join(destination_dir, os.path.basename(src))
        shutil.copy2(src, dst)
        print(f"✅ تم نقل: {path} ➜ {dst}")
    else:
        print(f"⚠️ لم يتم العثور على: {path}")
