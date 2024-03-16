from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base
from app.models.user_event import user_event


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    details = Column(String)
    location = Column(String)
    event_date = Column(Date)
    event_time = Column(Time)
    creation_at = Column(DateTime, default=datetime.utcnow)

    attendees = relationship("User", secondary=user_event, back_populates="events_registered", lazy='dynamic')
