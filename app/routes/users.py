from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.users import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from app.auth.auth import authenticate_user, create_access_token
from app.database.operations.users import check_existing_email,check_existing_username,create_user
router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", response_model=UserCreateResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
        User registration
    """
    db_email = check_existing_email(db, user.email)
    db_user = check_existing_username(db, user.username)

    if db_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already registered",
        )

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is taken",
        )

    return create_user(db, user)


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
