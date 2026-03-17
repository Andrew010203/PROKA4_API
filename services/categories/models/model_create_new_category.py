from pydantic import BaseModel
from datetime import datetime


class CreateNewCategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime