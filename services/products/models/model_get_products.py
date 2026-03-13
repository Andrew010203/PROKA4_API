from typing import List, Optional
from pydantic import BaseModel

class Product(BaseModel):
    category: str
    description: str
    id: int
    image_url: str
    name: str
    price: float
    rating: float
    reviews_count: int
    stock: int

class Meta(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int

class GetProductsResponse(BaseModel):
    data: List[Product]
    meta: Meta