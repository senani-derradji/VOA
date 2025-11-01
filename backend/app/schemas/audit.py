from pydantic import BaseModel
from datetime import datetime

class Action(BaseModel):
    action: str
    created_at: datetime

    class Config:
        from_attributes = True