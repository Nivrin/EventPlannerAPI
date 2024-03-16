from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.auth import get_current_user
from app.database.database import get_db
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from typing import List
from typing import Optional
from app.database.operations.events import (create_event, get_events, update_event,
                                            delete_event, register_user_for_event,
                                            unregister_user_for_event)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/CreateEvent/", response_model=EventResponse)
def create_event_handler(event: EventCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)
                         ):
    """
    Create new event
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return create_event(db, event, current_user)


@router.get("/GetEvents/", response_model=List[EventResponse])
def get_events_handler(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user),
                       location: Optional[str] = Query(None, description="Filter events by location/venue"),
                       sort_by: Optional[str] = Query(None, description="Sort events by date, popularity, or creation_time"),
                       event_id: Optional[int] = Query(None, description="Filter event by ID")
                       ):
    """
    Get all events
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return get_events(db, location, sort_by, event_id)


@router.put("/UpdateById/{event_id}", response_model= EventResponse)
def update_event_handler(
                 event_id: int,
                 event: EventUpdate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)
                 ):
    """
        update event
    """

    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return update_event(event_id,event,db,current_user)


@router.delete("/DeleteByID/{event_id}", response_model=EventResponse)
def delete_event_handler(
        event_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    """
        delete event by id
    """
    return delete_event(event_id, db, current_user)


@router.post("/RegisterEvent/{event_id}", response_model=EventResponse)
def register_user_for_event_handler(
        event_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
        ):
    """
    Register user for an event
    """
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return register_user_for_event(event_id, db, current_user)


@router.post("/UnregisterEvent/{event_id}", response_model=EventResponse)
def unregister_user_for_event_handler(
        event_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
        ):
    """
    Unregister user for an event
    """
    if current_user is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return unregister_user_for_event(event_id, db, current_user)
