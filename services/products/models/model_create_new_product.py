from pydantic import BaseModel
from datetime import datetime

class CreateProductResponse(BaseModel):
    category: str
    created_at: datetime
    description: str
    id: int
    image_url: str
    name: str
    price: float
    rating: float
    reviews_count: int
    stock: int