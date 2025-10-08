from pydantic import BaseModel
from datetime import datetime

class AuditOut(BaseModel):
    id: int
    user_id: int
    action: str
    details: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True