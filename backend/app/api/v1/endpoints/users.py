from fastapi import APIRouter, Depends, HTTPException
from app.core.deps import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/admin-only")
def admin_route(current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"msg": f"Welcome Admin {current_user['username']}"}

@router.get("/developer")
def developer_route(current_user=Depends(get_current_user)):
    if current_user["role"] not in ["admin", "developer"]:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return {"msg": f"Welcome Developer {current_user['username']}"}

@router.get("/me")
def user_info(current_user=Depends(get_current_user)):
    return {"username": current_user["username"], "role": current_user["role"]}
