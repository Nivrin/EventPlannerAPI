from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.users import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from app.auth.auth import authenticate_user, create_access_token
from app.database.operations.users import check_existing_email,check_existing_username,create_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["user"])


@router.post("/register", response_model=UserCreateResponse)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
        User registration

    """
    try:
        logger.info(f"Attempting to register user with email: {user.email} and username: {user.username}")
        db_email = await check_existing_email(db, user.email)
        db_user = await check_existing_username(db, user.username)

        if db_email:
            logger.error(f"User with email {user.email} already registered")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already registered",
            )

        if db_user:
            logger.error(f"Username {user.username} is already taken")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This username is taken",
            )
        created_user = await create_user(db, user)
        logger.info(f"User- {created_user.username}, {created_user.email} registered successfully")
        return created_user

    except Exception as e:
        logger.error(f"Error occurred during user registration: {e}")
        raise


@router.post("/login/", response_model=UserLoginResponse)
async def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """
        User login
    """
    try:
        logger.info(f"Attempting to login user with username: {user_data.username}")
        user = await authenticate_user(db, user_data.username, user_data.password)
        if not user:
            logger.error(f"Login failed for username: {user_data.username}. Incorrect username or password")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        logger.info(f"User with username: {user_data.username} logged in successfully")
        access_token = create_access_token(user.username)
        return {"access_token": access_token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Error occurred during user login: {e}")
        raise
