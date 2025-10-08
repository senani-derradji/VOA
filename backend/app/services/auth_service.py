from app.models.user import UserModel as USER
from app.core.security import get_password_hash, verify_password, create_access_token

def register_user(db, username: str, password: str, role: str = "user"):
    hashed_password = get_password_hash(password)
    user = USER(
        username=username, 
        password=hashed_password,  
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db, username: str, password: str):
    user = db.query(USER).filter(USER.username == username).first()
    if not user or not verify_password(password, user.password):
        return None
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    return access_token