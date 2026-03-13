from pydantic import BaseModel
from datetime import datetime

class UpdateProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    updated_at: datetime