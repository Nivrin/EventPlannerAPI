from app.database.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Table, Boolean


user_event = Table(
    'user_event',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('reminder_sent', Boolean, default=False)
)
