# file scr\crud\user_current.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.services.auth import auth_service
from fastapi.templating import Jinja2Templates
from jose import JWTError
from src.db.database import get_db
from sqlalchemy.orm import Session
from src.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth_service.decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
