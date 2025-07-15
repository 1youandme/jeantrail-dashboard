import os
from PIL import Image
import pytesseract
import shutil

# ⚙️ مسارات الصور
INPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\portable_blender"
OUTPUT_DIR = r"C:\Users\dell\JeanTrail_AI\images\filtered_portable_blender"

# 📂 إنشاء مجلد الإخراج إن لم يكن موجودًا
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 🔁 قراءة الصور واحدة تلو الأخرى
files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

print(f"🖼️ فحص {len(files)} صورة...")

text_counts = 0

for filename in files:
    image_path = os.path.join(INPUT_DIR, filename)
    image = Image.open(image_path)

    # 📖 استخراج النصوص باستخدام Tesseract
    text = pytesseract.image_to_string(image)

    # 🧠 الفلترة: استبعاد الصورة إن وُجد بها الكثير من النصوص (ما عدا لو كانت كلها كذلك)
    if len(text.strip()) < 20:
        shutil.copy(image_path, os.path.join(OUTPUT_DIR, filename))
    else:
        text_counts += 1

print(f"✅ تمت الفلترة: {len(os.listdir(OUTPUT_DIR))} صورة تم قبولها")
print(f"🚫 تم تجاهل {text_counts} صورة تحتوي على نصوص كثيرة")
