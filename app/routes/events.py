from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth import get_current_user
from app.database.database import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from typing import List
from datetime import datetime
from typing import Optional


router = APIRouter(prefix="/events", tags=["events"])


@router.post("/CreateEvent/", response_model=EventResponse)
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Create new event
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    event_dict = event.dict()
    db_event = Event(**event_dict)

    current_datetime = datetime.now()
    event_datetime = datetime.combine(db_event.event_date, db_event.event_time)
    if event_datetime <= current_datetime:
        raise HTTPException(status_code=400, detail="Cannot create past events")

    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


@router.get("/GetEvents/", response_model=List[EventResponse])
def get_events(db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user),
               location: Optional[str] = Query(None, description="Filter events by location/venue"),
               sort_by: Optional[str] = Query(None, description="Sort events by date, popularity, or creation time"),
               ):
    """
     Get all events
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    query = db.query(Event)

    if location:
        query = query.filter(Event.location == location)

    if sort_by:
        if sort_by.lower() == "date":
            query = query.order_by(Event.event_date)
        elif sort_by.lower() == "popularity":
            query = query.order_by(Event.attendees.count().desc())
        elif sort_by.lower() == "creation_time":
            query = query.order_by(Event.creation_at)
        else:
            raise HTTPException(status_code=400, detail="Invalid sorting option")

    return query.all()


@router.get("/GetByID/{event_id}", response_model=EventResponse)
def get_event_by_id(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
         Get event by id
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.put("/UpdateById/{event_id}", response_model= EventResponse)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        update event
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    print("Received request to update event with ID:", event)
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

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


@router.delete("/DeleteByID/{event_id}", response_model= EventResponse)
def delete_event_by_id(event_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
        delete event by id
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    db_event = db.query(Event).filter(Event.id == event_id).first()

    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    db.delete(db_event)

    db.commit()
    return db_event


@router.post("/RegisterEvent/{event_id}", response_model=EventResponse)
def register_user_for_event(event_id: int, db: Session = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    """
    Register user for an event
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    current_datetime = datetime.now()

    event_datetime = datetime.combine(event.event_date, event.event_time)
    if event_datetime <= current_datetime:
        raise HTTPException(status_code=400, detail="Cannot update past events")

    if event in current_user.events_attended:
        raise HTTPException(status_code=400, detail="User already registered for this event")
    print(current_user.username)
    current_user.events_attended.append(event)
    db.commit()
    db.refresh(current_user)
    return event