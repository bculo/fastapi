from datetime import timedelta
from http.client import HTTPException
from typing import Annotated

from fastapi import FastAPI, status, Query, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from auth import User, get_current_user, oauth2_scheme, fake_users_db, UserInDB, \
    get_current_active_user, Token, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from celery_instance import send_push_notification
from domain.exceptions import CoreException, NotFoundException
from routers import users, items, files
from sql import models
from sql.database import engine

app = FastAPI()


@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(items.router)
app.include_router(files.router)


@app.exception_handler(CoreException)
async def unicorn_exception_handler(request: Request, exc: CoreException):
    description = "Unknown exception" if exc.description is None else exc.description

    if type(exc) is NotFoundException:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=description)

    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=description)


@app.get("/")
async def throw_exception(word: Annotated[str, Query()]):
    print(word)
    send_push_notification.delay(word)
    return "ITS WORKS"


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
    return [{"item_id": "Foo", "owner": current_user.username}]






