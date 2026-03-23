from typing import List
from datetime import datetime

from pydantic import BaseModel, Field


class Item(BaseModel):
    price: float = Field(..., gt=0)
    product_id: int = Field(..., gt=0)
    product_name: str = Field(..., min_length=1)
    quantity: int = Field(..., gt=0)
    total: float = Field(..., gt=0)


class OrderResponse(BaseModel):
    created_at: datetime
    id: int = Field(..., gt=0)
    items: List[Item]
    status: str
    total: float = Field(..., gt=0)