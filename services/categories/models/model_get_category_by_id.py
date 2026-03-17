from pydantic import BaseModel

class CategoryResponse(BaseModel):
    description: str | None = None
    id: int
    name: str