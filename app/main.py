from fastapi.exceptions import RequestValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.auth import create_access_token, authenticate_user
from app.database.database import get_db
from app.routes import events, users
import uvicorn
from sqlalchemy.orm import Session


app = FastAPI(debug=True)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/")
async def health_check():
    return {"status": "UP"}


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db,form_data.username, form_data.password)
    print("fsafassffas")
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}


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
