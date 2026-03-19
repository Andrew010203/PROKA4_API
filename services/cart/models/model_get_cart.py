from typing import List, Optional
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    price: float
    product_id: int
    product_name: str
    quantity: int
    total: float


class GetCartResponse(BaseModel):
    count: int
    items: List[Item]
    total: float