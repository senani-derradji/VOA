# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import auth, secrets, users, logs


api_router = APIRouter()


api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(secrets.router, prefix="/secrets", tags=["Secrets"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(logs.router, prefix="/logs", tags=["Logs"])