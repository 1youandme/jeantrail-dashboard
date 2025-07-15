from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import products

app = FastAPI()

# تفعيل الـ CORS علشان React يقدر يوصل للـ API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# تضمين المسارات من ملف المنتجات
app.include_router(products.router)

# نقطة اختبار الاتصال
@app.get("/ping")
def ping():
    return {"message": "✅ Hello from JeanTrail Backend!"}
