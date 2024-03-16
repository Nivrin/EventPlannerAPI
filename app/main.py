import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request

from app.auth.auth import authenticate_user, create_access_token
from app.database.database import create_database, get_db
from app.routes import events, users
from app.tasks.background_tasks import send_reminders
from app.utils.logger import setup_logging
import uvicorn

SCHEDULER_INTERVAL_MINUTES = 1
LOG_FILE_PATH = "./data_and_logs/logs/app.log"


setup_logging()

app = FastAPI()

scheduler = BackgroundScheduler()


logging.info('Application started')

create_database()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(events.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup_event():
    scheduler.add_job(send_reminders, "interval", minutes=SCHEDULER_INTERVAL_MINUTES)
    scheduler.start()


@app.post("/schedule-reminder")
async def schedule_reminder(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_reminders)
    return {"message": "Reminder scheduled"}


@app.get("/")
async def health_check():
    return {"status": "UP"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await authenticate_user(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/logs")
async def get_logs():
    if not os.path.exists(LOG_FILE_PATH):
        raise HTTPException(status_code=404, detail="Log file not found")

    return FileResponse(LOG_FILE_PATH)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_msg = exc.errors()[0]['msg']

    if error_msg == 'Field required':
        error_field = exc.errors()[0]['loc'][1]
        return JSONResponse(status_code=422, content={"detail": [{"msg": error_msg, "field": error_field}]})

    return JSONResponse(status_code=422, content={"detail": [{"msg": error_msg}]})


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)