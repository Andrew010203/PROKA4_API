from typing import List
from datetime import datetime
from pydantic import BaseModel


class Review(BaseModel):
    author: str
    comment: str
    created_at: datetime
    id: int
    product_id: int
    rating: int


class ReviewListResponse(BaseModel):
    comments: List[Review]