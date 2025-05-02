from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str]
    price_cents: int
    image_url: Optional[str]
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price_cents: Optional[int]
    image_url: Optional[str]
    stock: Optional[int]
