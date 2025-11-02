from pydantic import BaseModel, validator
from datetime import datetime

actions = (
    "login",
    "register",
    "create_user",
    "list_users",
    "read_user",
    "update_user",
    "delete_user",
    "create_secret",
    "list_secrets",
    "read_secret",
    "list_secrets_versions",
    "update_secret",
    "delete_secret"
)


class Action(BaseModel):
    action: str
    @validator("action")
    def validate_action(cls, value):
        if value.startswith(actions): pass
    created_at: datetime


    class Config:
        from_attributes = True