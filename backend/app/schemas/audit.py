from pydantic import BaseModel, validator
from datetime import datetime
from fastapi import HTTPException

class Action(BaseModel):
    action: str 
    @validator("action")
    def validate_action(cls, action):
        permessions = ["create", "update", "delete", "read", "list"]
        additions = ["forbidden_access", "login"]
        if (action == permession or 
               action.startswith(f"{permession}_user")  or 
               action.startswith(f"{permession}_secret") or
               action.endswith(addition for addition in additions)
               for permession in permessions): return action
        raise HTTPException("Invalid action type")
    created_at: datetime

    class Config:
        from_attributes = True