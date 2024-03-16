from app.database.database import Base
from app.models.users_events import user_event
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    events_created = relationship("Event", back_populates="creator")
    events_registered = relationship("Event", secondary=user_event, back_populates="participants", lazy='dynamic')
