from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    image: Optional[str] = None
