from pydantic import BaseModel

class SandboxResetResponse(BaseModel):
    message: str
    resource: str