from pydantic import BaseModel
from datetime import datetime


class UpdateResponse(BaseModel):
    description: str
    id: int
    name: str
    updated_at: datetime | None = None