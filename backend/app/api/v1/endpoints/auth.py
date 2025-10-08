# app/api/v1/endpoints/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserModel
from app.core.security import create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password
from slowapi import Limiter
from slowapi.util import get_remote_address


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/login")
@limiter.limit("10/hour", error_message="to many requests (we have blocked you 1H)")
async def login(request: Request,
          form_data: OAuth2PasswordRequestForm = Depends(), 
          db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail=f"Invalid credentials")
    access_token = create_access_token({"sub": user.username, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}