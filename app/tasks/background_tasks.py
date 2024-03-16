from datetime import datetime, timedelta
from sqlalchemy import func

from app.database.database import get_db
from app.models.events import Event
from app.models.users_events import user_event
from app.utils.email import send_email_reminder

def send_reminders():
    """
    Function to send reminders for events occurring within the next 30 minutes.
    """

    db = next(get_db())
    current_datetime = datetime.now()
    time_threshold = current_datetime + timedelta(minutes=30)

    event_datetime = func.datetime(Event.event_date, Event.event_time)

    events = db.query(Event).filter(event_datetime >= current_datetime, event_datetime <= time_threshold).all()

    for event in events:
        attendees = event.participants
        for attendee in attendees:
            if db.query(user_event).filter_by(user_id=attendee.id, event_id=event.id, reminder_sent=False).first():
                send_email_reminder(event, attendee)
                db.execute(user_event.update().where(
                    user_event.c.user_id == attendee.id and user_event.c.event_id == event.id).values(
                    reminder_sent=True))
                db.commit()

    db.close()