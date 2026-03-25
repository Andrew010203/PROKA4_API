from pydantic import BaseModel
from datetime import datetime


class UpdateReviewResponse(BaseModel):
    author: str
    comment: str
    id: int
    product_id: int
    rating: int
    updated_at: datetime