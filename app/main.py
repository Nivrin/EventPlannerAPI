from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from app.auth.auth import create_access_token, authenticate_user
from app.database.database import get_db, create_database  # Import create_database function
from app.routes import events, users
import uvicorn
from sqlalchemy.orm import Session
# from app.tasks.reminder_tasks import celery_
from app.utils.logger import  setup_logging
import logging
import os


app = FastAPI(debug=True)

setup_logging()
logging.info('Application started')
LOG_FILE_PATH = "./data_and_logs/logs/app.log"

create_database()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# app.config = {
#     "CELERY_BROKER_URL": "redis://localhost:6379/0",
# }

# @app.on_event("startup")
# async def startup_event():
#     # Start the Celery scheduler when the FastAPI application starts
#     celery_.conf.update(app.config)


@app.get("/")
async def health_check():
    return {"status": "UP"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db,form_data.username, form_data.password)
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


app.include_router(events.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("app", host="127.0.0.1", port=8000, reload=True)
