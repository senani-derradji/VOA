# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserModel
from app.core.security import create_access_token, verify_password, create_refresh_token, SEC_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import timedelta
from app.core.deps import get_current_user
from app.models.user import UserModel
from app.utils.RandomNumber import random_integer as rand
from app.services.audit import log_action
from jose import jwt, JWTError



router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/login")
@limiter.limit(f"{rand}/hour", error_message="to many requests (we have blocked you 1H)")
async def login(request: Request,
          form_data: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail=f"Invalid credentials")
    
    access_token_expires = timedelta(minutes=30)
    refresh_token_expires = timedelta(days=7)

    access_token = create_access_token({"sub": user.username, "role": user.role}, access_token_expires)
    refresh_token = create_refresh_token({"sub": user.username, "role": user.role}, refresh_token_expires)

    log_action(db, user.id, f"login")


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SEC_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=400, detail="Invalid token type")

        username = payload.get("sub")
        new_access_token = create_access_token({"sub": username})

        return {"access_token": new_access_token, "token_type": "bearer"}

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

@router.post("/register")
def register(
    username: str, 
    password: str, 
    role: str, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
    ):
    
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_user = UserModel(
        username=username, 
        password=password, 
        role=role
        )
    log_action(db, current_user.id, f"create_user ({new_user.username})")
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}