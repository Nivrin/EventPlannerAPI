import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.auth import get_current_user
from app.database.database import get_db
from app.database.operations.events import (create_event, delete_event, get_events,
                                            register_user_for_event, unregister_user_for_event,
                                            update_event)
from app.models.users import User
from app.schemas.events import EventCreate, EventResponse, EventUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/CreateEvent/", response_model=EventResponse)
async def create_event_handler(event: EventCreate,
                         db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_user)
                         ):
    """
    Create new event
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        event_data = await create_event(db, event, current_user)

        logger.info(f"Event '{event_data.title}' created by user '{current_user.username}'")
        return event_data

    except Exception as e:
        logger.error(f"Error occurred during event creation: {e}")
        raise


@router.get("/GetEvents/", response_model=List[EventResponse])
async def get_events_handler(db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_user),
                       location: Optional[str] = Query(None, description="Filter events by location/venue"),
                       sort_by: Optional[str] = Query(None, description="Sort events by date, popularity, or creation_time"),
                       event_id: Optional[int] = Query(None, description="Filter event by ID")
                       ):
    """
    Get all events
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        events = await get_events(db, location, sort_by, event_id)

        logger.info(f"{len(events)} events retrieved for user '{current_user.username}'")
        return events

    except Exception as e:
        logger.error(f"Error occurred while retrieving events: {e}")
        raise


@router.put("/UpdateById/{event_id}", response_model=EventResponse)
async def update_event_handler(
                 event_id: int,
                 event: EventUpdate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)
                 ):
    """
        update event
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        updated_event = await update_event(event_id, event, db, current_user)

        logger.info(f"Event '{updated_event.title}' updated by user '{current_user.username}'")
        return updated_event

    except Exception as e:
        logger.error(f"Error occurred during event update: {e}")
        raise


@router.delete("/DeleteByID/{event_id}", response_model=EventResponse)
async def delete_event_handler(
        event_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    """
        delete event by id
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        deleted_event = await delete_event(event_id, db, current_user)

        logger.info(f"Event '{deleted_event.title}' deleted by user '{current_user.username}'")
        return deleted_event

    except Exception as e:
        logger.error(f"Error occurred during event deletion: {e}")
        raise


@router.post("/RegisterEvent/{event_id}", response_model=EventResponse)
async def register_user_for_event_handler(
        event_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
        ):
    """
    Register user for an event
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        registered_event = await register_user_for_event(event_id, db, current_user)

        logger.info(f"User '{current_user.username}' registered for event '{registered_event.title}'")
        return registered_event

    except Exception as e:
        logger.error(f"Error occurred during user registration for event: {e}")
        raise


@router.post("/UnregisterEvent/{event_id}", response_model=EventResponse)
async def unregister_user_for_event_handler(
        event_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
        ):
    """
    Unregister user for an event
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        unregistered_event = await unregister_user_for_event(event_id, db, current_user)

        logger.info(f"User '{current_user.username}' unregistered from event '{unregistered_event.title}'")
        return unregistered_event

    except Exception as e:
        logger.error(f"Error occurred during user unregistration for event: {e}")
        raise
