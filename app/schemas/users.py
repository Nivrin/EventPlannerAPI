from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr = Field(..., examples=["user@example.com"])
    username: str = Field(..., max_length=50, examples =["example_user"])
    password: str = Field(..., max_length=100, examples=["password123"])

    class Config:
        extra = "forbid"


class UserLogin(BaseModel):
    username: str = Field(..., max_length=50, examples =["example_user"])
    password: str = Field(..., max_length=100, examples=["password123"])

    class Config:
        extra = "forbid"


class UserCreateResponse(BaseModel):
    email: EmailStr = Field(..., examples =["user@example.com"])
    username: str = Field(..., max_length=50, examples =["example_user"])
    password: str = Field(..., max_length=100, examples=["password123"])


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    username: str = Field(..., max_length=50)
