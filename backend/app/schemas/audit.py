from pydantic import BaseModel, validator
from datetime import datetime
from fastapi import HTTPException

class AuditOut(BaseModel):
    id: int
    user_id: int
    action: str 
    @validator("action")
    def validate_action(cls, action):
        permessions = ["create", "update", "delete", "read", "list", "login"]
        if action not in permessions:
            HTTPException(f"the action is just one of : {permessions}")
    created_at: datetime

    class Config:
        from_attributes = True