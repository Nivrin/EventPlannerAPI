from datetime import datetime, timedelta
from celery import Celery
from app.database.database import get_db
from app.models.events import Event


celery_ = Celery("tasks", broker="redis://localhost:6379/0")


@celery_.task
def send_event_reminders():
    with get_db() as db:
        current_time = datetime.now()
        future_time = current_time + timedelta(minutes=30)
        events_to_remind = db.query(Event).filter(Event.event_datetime.between(current_time, future_time)).all()

        for event in events_to_remind:
            attendees_emails = [attendee.email for attendee in event.attendees]
            for attendee_email in attendees_emails:
                print(f"{attendee_email} - Reminder: Event '{event.title} stats in 30 mintes.")
