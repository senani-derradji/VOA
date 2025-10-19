from pydantic import BaseModel, Field, validator
from datetime import datetime
from fastapi import HTTPException


class SecretsCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    @validator("name")
    def Validate_secret_name(cls, name):
        if any(char.isdigit() for char in name): raise HTTPException("Secret name cannot contain numbers")
        return name
    value: str = Field(min_length=1, max_length=256)
    environment: str = "dev"
    @validator("environment")
    def Validate_environment(cls, environment):
        if environment not in ["dev", "test", "prod"]: HTTPException("dev or test or prod")

class SecretsUpdate(BaseModel):
    name: str  = None
    value: str = None
    environment: str = None

class SecretsOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True