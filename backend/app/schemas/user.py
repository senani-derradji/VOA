from pydantic import BaseModel, Field, validator
from enum import Enum
from fastapi import HTTPException

class RoleEnum(str, Enum):
    admin = "admin"
    developer = "developer"

class UserBase(BaseModel):
    username: str = Field(min_length=10, max_length=26)
    role: RoleEnum = RoleEnum.developer

    @validator("username")
    def validate_username(cls, value):
        if any(char.isupper() for char in value): raise HTTPException(status_code=400, detail="Username cannot contain uppercase letters")
        if not any(char.isalnum() for char in value): raise HTTPException(status_code=400, detail="Username can only contain letters and numbers")
        return value
    
    @validator("role")
    def validate_role(cls, value):
        if value not in ["admin", "developer"]: raise HTTPException(status_code=400, detail="Invalid role")
        return value



class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=26)

    @validator("password")
    def validate_password(cls, value):
        if not any(char.isdigit() for char in value): raise HTTPException(status_code=400, detail="Password must contain at least one digit")
        if not any(char.isalpha() for char in value): raise HTTPException(status_code=400, detail="Password must contain at least one letter")
        if not any(char.isupper() for char in value): raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")
        if not any(char.islower() for char in value): raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")
        return value


class UserOut(UserBase):
    id: int = Field(gt=0)
    
    class Config:
        from_attributes = True