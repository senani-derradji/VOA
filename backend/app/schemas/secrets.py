from pydantic import BaseModel, Field, validator
from datetime import datetime
from fastapi import HTTPException


class SecretsCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    @validator("name")
    def Validate_secret_name(cls, name):
        if any(char.isdigit() for char in name): raise HTTPException("Secret name cannot contain numbers")
        if len(name) > 50 : raise HTTPException("Secret name cannot be longer than 50 characters")
        return name
    value: str = Field(min_length=1, max_length=256)
    @validator("value")
    def Validate_secret_value(cls, value):
        if len(value) > 256 : raise HTTPException("Secret value cannot be longer than 256 characters")
        return value
    environment: str = "dev"
    @validator("environment")
    def Validate_environment(cls, environment):
        if environment not in ["dev", "test", "prod"]: HTTPException("environment should be just : dev or test or prod")

class SecretsUpdate(BaseModel):
    name: str  = None
    value: str = None
    environment: str = None
    @validator("environment")
    def Validate_environment(cls, environment):
        if environment not in ["dev", "test", "prod"]: HTTPException("environment should be just : dev or test or prod")


class SecretsOut(BaseModel):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True