from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.events import Event
from app.models.users import User
from datetime import datetime
from app.schemas.events import EventCreate, EventUpdate
from sqlalchemy import func
from app.models.users_events import user_event


async def create_event(db: Session, event_data: EventCreate, current_user: User):
    event_dict = event_data.dict()
    event_dict["creator_id"] = current_user.id
    db_event = Event(**event_dict)

    current_datetime = datetime.now()
    event_datetime = datetime.combine(db_event.event_date, db_event.event_time)
    if event_datetime <= current_datetime:
        raise HTTPException(status_code=400, detail="Cannot create past events")

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


async def get_events(db: Session, location: str = None, sort_by: str = None, event_id: int = None):
    if event_id:
        event = db.query(Event).filter(Event.id == event_id).first()
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return [event]

    query = db.query(Event)

    if location:
        query = query.filter(Event.location == location)

    if sort_by:
        if sort_by.lower() == "date":
            query = query.order_by(Event.event_date.desc(), Event.event_time.desc())
        elif sort_by.lower() == "popularity":
            query = query.outerjoin(Event.participants).group_by(Event.id).order_by(func.count(User.id).desc())
        elif sort_by.lower() == "creation_time":
            query = query.order_by(Event.creation_at.desc())
        else:
            raise HTTPException(status_code=400, detail="Invalid sorting option")

    return query.all()


async def update_event(event_id: int, event: EventUpdate, db: Session, current_user: User):

    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the creator of this event")

    current_datetime = datetime.now()
    event_datetime = datetime.combine(db_event.event_date, db_event.event_time)
    if event_datetime <= current_datetime:
        raise HTTPException(status_code=400, detail="Cannot update past events")

    for attr, value in event.dict().items():
        if value is not None:
            setattr(db_event, attr, value)
    db.commit()
    db.refresh(db_event)
    return db_event


async def delete_event(event_id: int, db: Session, current_user: User):
    """
        delete event by id
    """

    db_event = db.query(Event).filter(Event.id == event_id).first()

    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    if db_event.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the creator of this event")

    db.delete(db_event)

    db.commit()
    return db_event


async def register_user_for_event(
        event_id: int,
        db: Session,
        current_user: User,
        ):
    """
    Register user for an event
    """

    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    current_datetime = datetime.now()

    event_datetime = datetime.combine(event.event_date, event.event_time)
    if event_datetime <= current_datetime:
        raise HTTPException(status_code=400, detail="Cannot register past events")

    if event in current_user.events_registered:
        raise HTTPException(status_code=400, detail="User already registered for this event")

    current_user.events_registered.append(event)
    db.commit()
    db.refresh(current_user)
    return event


async def unregister_user_for_event(
        event_id: int,
        db: Session,
        current_user: User
        ):
    """
    Unregister user for an event
    """

    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    current_datetime = datetime.now()

    event_datetime = datetime.combine(event.event_date, event.event_time)
    if event_datetime <= current_datetime:
        raise HTTPException(status_code=400, detail="Cannot unregister past events")

    if event not in current_user.events_registered:
        raise HTTPException(status_code=400, detail="User already not registered for this event")

    db.execute(user_event.delete().where(user_event.c.user_id == current_user.id)
               .where(user_event.c.event_id == event_id))
    db.commit()
    db.refresh(current_user)

    return event

