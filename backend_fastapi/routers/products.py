from fastapi import APIRouter
from services.supabase_service import get_products_from_supabase

router = APIRouter(prefix="/api", tags=["Products"])

@router.get("/products")
def get_products():
    return get_products_from_supabase()
