from typing import List, Optional
from pydantic import BaseModel

class Category(BaseModel):
    description: Optional[str] = None
    id: int
    name: str

class GetCategoriesResponse(BaseModel):
    categories: List[Category]