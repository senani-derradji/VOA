from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.extentions.database import get_db
from app.models.user import UserModel
from app.core.security import get_password_hash
from app.core.deps import get_current_user
from app.services.audit import log_action
from app.schemas.user import UserCreate, UserOut
from app.RBAC.roles import admin_required, CEO_required
from datetime import datetime, timedelta



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

    if role == "admin":
        if CEO_required(current_user, f"register_user_{username}"): pass
    elif role == "developer":
        if admin_required(current_user, f"register_user_{username}"): pass
    else:
        raise HTTPException(status_code=400, detail="Invalid role")


    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = get_password_hash(password)
    new_user = UserModel(
        username=username,
        password=hashed_password,
        role=role,
        created_at=datetime.utcnow(),
        expired_at=datetime.utcnow() + timedelta(days=90)
        )
    log_action(db, current_user.id, f"create_user")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {new_user.username} created successfully"}


@router.get("/")
def get_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    if CEO_required(current_user, f"users_list") or admin_required(current_user, f"users_list"):
        pass

    users = db.query(UserModel).all()
    return users


@router.put("/{user_id}")
def change_user_role(
    data_form : UserOut,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user_id = data_form.id
    username = data_form.username
    role = db.query(UserModel).filter(UserModel.id == user_id).first().role


    if role == "admin" or role == "CEO":
        if CEO_required(current_user, f"update_admin_ceo_{username}"): pass
    elif role == "developer":
        if admin_required(current_user, f"register_user_{username}"): pass
    else:
        raise HTTPException(status_code=400, detail="Invalid role")

    new_role = data_form.role
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot change your own role")


    user.role = new_role

    log_action(db, current_user.id, f"update_user_role")
    db.commit()
    return {"message": f"User role updated to {new_role}"}


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):


    role = db.query(UserModel).filter(UserModel.id == user_id).first().role


    if role == "admin" or role == "CEO":
        if CEO_required(current_user, f"update_admin_ceo_{user_id}"): pass
    elif role == "developer":
        if admin_required(current_user, f"register_user_{user_id}"): pass
    else:
        raise HTTPException(status_code=400, detail="Invalid role")


    user = db.query(UserModel).filter(UserModel.id == user_id).first()


    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")

    db.delete(user)
    log_action(db, current_user.id, f"delete_user")
    db.commit()
    return {"message": "User deleted successfully"}

