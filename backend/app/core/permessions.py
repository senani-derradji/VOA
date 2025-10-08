from fastapi import HTTPException, Depends, status
from app.core.deps import get_current_user

def admin_required(current_user: dict = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden",
        )
    return current_user

def developer_required(current_user: dict = Depends(get_current_user)):
    if current_user.role not in ["admin", "developer"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden",
        )
    return current_user
