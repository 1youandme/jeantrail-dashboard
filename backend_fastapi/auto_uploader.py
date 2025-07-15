import tkinter as tk
from tkinter import messagebox
import requests
import json

# نموذج بيانات وهمي للإرسال (هيتغير لاحقًا بعد إدخال الزحف الحقيقي)
def send_to_api(product):
    try:
        response = requests.post("http://127.0.0.1:8000/products", json=product)
        if response.status_code == 200:
            messagebox.showinfo("تم", "تم إرسال المنتج بنجاح")
        else:
            messagebox.showerror("فشل", f"فشل في الإرسال: {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("خطأ", str(e))

# UI
def submit():
    keyword = entry.get()
    if not keyword:
        messagebox.showwarning("تنبيه", "من فضلك أدخل الكلمة المفتاحية")
        return

    # Placeholder لزحف المنتج (هندمجه لاحقًا)
    product = {
        "title": f"منتج {keyword}",
        "price": "12.99",
        "min_order": "10",
        "colors": ["أسود", "أبيض"],
        "sizes": ["M", "L", "XL"],
        "shipping_cost": "5.00",
        "shipping_time": "7 أيام",
        "supplier": "شركة وهمية",
        "image_url": "https://example.com/product.jpg",
        "description": f"وصف تلقائي للمنتج: {keyword}"
    }

    send_to_api(product)

# تصميم الواجهة
root = tk.Tk()
root.title("رفع منتجات تلقائيًا لـ FastAPI")
root.geometry("400x200")

tk.Label(root, text="الكلمة المفتاحية للمنتج:").pack(pady=10)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)

tk.Button(root, text="رفع المنتج", command=submit).pack(pady=20)

root.mainloop()
