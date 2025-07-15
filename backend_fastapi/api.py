from fastapi import FastAPI, HTTPException
from models import Product
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "products"

app = FastAPI()

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

@app.post("/products/")
async def create_product(product: Product):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            headers=headers,
            json=product.dict()
        )
        if response.status_code == 201:
            return {"status": "success", "product": product}
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.get("/products/")
async def get_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?select=*",
            headers=headers
        )
        if response.status_code == 200:
            return response.json()
        raise HTTPException(status_code=response.status_code, detail=response.text)
