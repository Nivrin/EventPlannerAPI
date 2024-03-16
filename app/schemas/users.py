from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime, time
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=30, examples =["user@example.com"])
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
    email: EmailStr = Field(..., max_length=30, examples =["user@example.com"])
    username: str = Field(..., max_length=50, examples =["example_user"])
    password: str = Field(..., max_length=100, examples=["password123"])


class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
