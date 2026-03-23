from pydantic import BaseModel
from datetime import datetime


class UpdateOrderResponse(BaseModel):
    id: int
    status: str
    total: float
    updated_at: datetime