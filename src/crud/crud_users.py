# file scr\crud\users.py

from sqlalchemy.orm import Session
from src.db.models import User, Role  # Убедитесь, что Role импортирована
from src.schemas.schemas_user import UserModel

async def create_user(body: UserModel, db: Session):
    admin_exists = db.query(User).filter(User.role == Role.admin).first()
    if admin_exists:
        new_user = User(**body.dict(), role=Role.user)
    else:
        new_user = User(**body.dict(), role=Role.admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def get_user_by_email(email: str, db: Session) -> User | None:
    return db.query(User).filter_by(email=email).first()

async def update_token(user: User, refresh_token: str, db: Session):
    user.refresh_token = refresh_token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    if user:
        user.confirmed = True
        db.commit()

# Новые функции для управления пользователями

async def get_user_by_id(user_id: int, db: Session) -> User | None:
    return db.query(User).filter_by(id=user_id).first()

async def delete_user(user_id: int, db: Session):
    user = await get_user_by_id(user_id, db)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

async def get_all_users(db: Session):
    return db.query(User).all()
