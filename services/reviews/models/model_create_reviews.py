from pydantic import BaseModel
from datetime import datetime


class ReviewResponse(BaseModel):
    author: str
    comment: str
    created_at: datetime
    id: int
    product_id: int
    rating: int