from pydantic import BaseModel
from datetime import datetime

class SecretsBase(BaseModel):
    name: str
    value: str
    environment: str = "dev"


class SecretsCreate(SecretsBase):
    pass

class SecretsUpdate(BaseModel):
    name: str  = None
    value: str = None
    environment: str = None

class Secrets(SecretsBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True