from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.user import User
from app.schemas.users import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from app.auth.auth import authenticate_user, create_access_token, get_password_hash

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", response_model=UserCreateResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
        User registration
    """
    db_email = db.query(User).filter(User.email == user.email).first()
    db_user = db.query(User).filter(User.username == user.username).first()

    if db_email :
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already registered",
        )

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is taken",
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login/", response_model=UserLoginResponse)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """
        User login
    """
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}
