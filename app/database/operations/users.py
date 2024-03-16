from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth import authenticate_user, create_access_token, get_password_hash
from app.schemas.users import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse


def check_existing_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def check_existing_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
