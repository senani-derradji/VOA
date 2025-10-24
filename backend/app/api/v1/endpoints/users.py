from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import UserModel
from app.core.security import get_password_hash
from app.core.deps import get_current_user
from app.services.audit import log_action
from app.schemas.user import UserCreate, UserOut
from app.utils.logging_logs import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post(
    "/register",
    summary="Register a new user",
    description="Creates a new user account with username, password, and role."
)
def register(
    data_form: UserCreate, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
    ):

    username = data_form.username
    password = data_form.password
    role = data_form.role


    
    if current_user.role != "admin":
        logger.warning(f"{current_user.username} Tried to Add New User {username}")
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
    log_action(db, current_user.id, f"create_user")
    logger.info(f"{current_user.username} Added New User {username}")
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {new_user.username} created successfully"}

@router.get("/")
def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        logger.warning(f"{current_user.username} Tried to get Users List")
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    users = db.query(UserModel).all()
    logger.info(f"{current_user.username} are get list of users")
    return users


@router.put("/{user_id}")
def change_user_role(
    data_form : UserOut,
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    user_id = data_form.id
    new_role = data_form.role
    
    if current_user.role != "admin" and current_user.id != user_id:
        logger.critical(f"{current_user.username} Tried to change Role of User:{user_id}")
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")
    
    
    user.role = new_role

    log_action(db, current_user.id, f"update_user_role")
    logger.info(f"{current_user.username} updates the role {new_role} successfully")
    db.commit()
    return {"message": f"User role updated to {new_role}"}


@router.delete("/{user_id}")
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        logger.warning(f"{current_user.username} Tried to delete User:{user_id}")
        raise HTTPException(status_code=403, detail="Access forbidden")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    
    db.delete(user)
    log_action(db, current_user.id, f"delete_user")
    logger.info(f"{current_user.username} are deleted the user:{user_id} seccessfully")
    db.commit()
    return {"message": "User deleted successfully"}

