import os
import google.generativeai as genai
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ لم يتم العثور على مفتاح API لـ Gemini في ملف .env")

# إعداد Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash-latest")

# إدخال بيانات المنتج
print("🔹 أدخل معلومات المنتج:")
title = input("اسم المنتج: ").strip()
features = input("مواصفات المنتج (مميزات - استخدامات): ").strip()

# إنشاء البرومبت
prompt = f"""
اكتب وصفًا تسويقيًا احترافيًا لمنتج يُدعى "{title}"، بناءً على المواصفات التالية:
{features}

الشروط:
- استخدم لغة جذابة.
- لا تكرر اسم المنتج كثيرًا.
- استخدم فقرات قصيرة.
- أضف نداءًا للشراء Call To Action.
"""

# توليد النص
response = model.generate_content(prompt)
description = response.text.strip()

# عرض النتيجة
print("\n✅ الوصف التسويقي الناتج:\n")
print(description)
