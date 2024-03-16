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


@router.post("/CreateEvents/", response_model=List[EventResponse])
async def create_event_handler(events: List[EventCreate],
                               db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)
                               ):
    """
    Create multiple events
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        created_events = []
        for event in events:
            created_event = await create_event(db, event, current_user)
            created_events.append(created_event)

        logger.info(f"{len(created_events)} events created by user '{current_user.username}'")
        return created_events

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
    Get events
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


@router.put("/UpdateEvents/", response_model=List[EventResponse])
async def update_event_handler(events: List[EventUpdate],
                               db: Session = Depends(get_db),
                               current_user: User = Depends(get_current_user)
                               ):
    """
        update multiple event
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        updated_events = []
        for event in events:
            updated_event = await update_event(event.id, event, db, current_user)
            updated_events.append(updated_event)

        logger.info(f"{len(updated_events)} events updated by user '{current_user.username}'")
        return updated_events
    except Exception as e:
        logger.error(f"Error occurred during event update: {e}")
        raise


@router.delete("/DeleteEvents/", response_model=List[EventResponse])
async def delete_event_handler(
        event_ids: List[int],
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
    """
        Delete multiple events by their IDs
    """
    try:
        if current_user is None:
            raise HTTPException(status_code=401, detail="Not authenticated")

        deleted_events = []
        for event_id in event_ids:
            deleted_event = await delete_event(event_id, db, current_user)
            deleted_events.append(deleted_event)

        logger.info(f"{len(deleted_events)} events deleted by user '{current_user.username}'")
        return deleted_events

    except Exception as e:
        logger.error(f"Error occurred during event deletion: {e}")
        raise


@router.post("/RegisterEvent/{event_id}", response_model=EventResponse)
async def register_user_for_event_handler(event_id: int,
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
