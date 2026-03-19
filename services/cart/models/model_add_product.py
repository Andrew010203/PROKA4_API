from pydantic import BaseModel
from datetime import datetime


class AddProductResponse(BaseModel):
    created_at: datetime
    id: int
    price: float
    product_id: int
    product_name: str
    quantity: int
    total: float