from datetime import date, datetime, time
from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.users import UserResponse


class EventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=50, examples =["string"])
    details: str = Field(..., max_length=100, examples =["string"])
    location: str = Field(..., max_length=100, examples =["string"])
    event_date: date = Field(..., examples = ["YYYY-MM-DD"])
    event_time: time = Field(..., examples = ["HH:MM"])

    class Config:
        extra = "forbid"


class EventUpdate(BaseModel):
    id: int = Field(None, examples=["int"])
    title: Optional[str] = Field(None, examples =["string"])
    details: Optional[str] = Field(None, examples =["string"])
    location: Optional[str] = Field(None, examples =["string"])
    event_date: Optional[date] = Field(None, examples = ["YYYY-MM-DD"])
    event_time: Optional[time] = Field(None, examples = ["HH:MM"])

    class Config:
        extra = "forbid"


class EventResponse(BaseModel):
    id: Optional[int]
    title: Optional[str]
    details: Optional[str]
    location: Optional[str]
    event_date: Optional[date]
    event_time: Optional[time]
    creation_at: Optional[datetime]
    creator: Optional[UserResponse]
    participants: Optional[List[UserResponse]]
