from sqlalchemy.orm import Session

from app.auth.auth import get_password_hash
from app.models.users import User
from app.schemas.users import UserCreate


async def check_existing_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


async def check_existing_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


async def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
