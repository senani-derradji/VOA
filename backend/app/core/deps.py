from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.core.security import SEC_KEY, ALGORITHM
from app.models.user import UserModel as User
from app.extentions.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)):

    credentials_exception = HTTPException( status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")

    try:
        payload = jwt.decode(token, SEC_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user