import logging
from app.models.events import Event
from app.models.users import User

logger = logging.getLogger(__name__)


def send_email_reminder(event: Event, attendee: User):
    logger.info(f"Sending reminder for event '{event.title}' to attendee '{attendee.username}'. The event is starting in 30 minutes")
