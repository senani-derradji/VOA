from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserModel
from app.core.security import get_password_hash
from app.core.deps import get_current_user
from app.services.audit import log_action


router = APIRouter()

# Add these endpoints to your existing users.py

@router.post(
    "/register",
    summary="Register a new user",
    description="Creates a new user account with username, password, and role."
)
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
    
    hashed_password = get_password_hash(password)
    new_user = UserModel(
        username=username, 
        password=hashed_password, 
        role=role
        )
    log_action(db, current_user.id, f"create_user ({new_user.username})")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {new_user.username} created successfully"}

@router.get("/")
def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get all users (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    users = db.query(UserModel).all()
    return users


@router.put("/{user_id}")
def change_user_role(
    user_id: int, 
    new_role: str, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """
    Change user role (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    valid_roles = ["admin", "developer", "viewer"]
    if new_role not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    user.role = new_role
    log_action(db, current_user.id, f"change_user_role ({user.username} to {new_role})")
    db.commit()
    return {"message": f"User role updated to {new_role}"}


@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    """
    Delete user (Admin only)
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    log_action(db, current_user.id, f"delete_user ({user.username})")
    db.commit()
    return {"message": "User deleted successfully"}
