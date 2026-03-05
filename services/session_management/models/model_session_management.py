from typing import Optional
from pydantic import BaseModel


class Limits(BaseModel):
    max_resource_size: int
    max_resources_per_type: int
    ttl: str


class SessionManagementResponse(BaseModel):
    bearer_token: str
    is_authenticated: bool
    limits: Limits
    session_id: str
    storage: str
    user_id: int