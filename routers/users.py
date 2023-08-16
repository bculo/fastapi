from typing import Annotated

from fastapi import APIRouter, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from starlette import status

from celery_instance import celery

from domain.exceptions import NotFoundException, CoreException

from sql import crud, schemas
from sql.dependencies import get_db
from sql.schemas import Message

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/create/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise CoreException("Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/page")
async def user_page(take: Annotated[int, Query()], skip: Annotated[int, Query()], db: Session = Depends(get_db)):
    users = crud.get_users(db, skip, take)
    if len(users) == 0:
        return []
    return users


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}


@router.post("/message/all", status_code=status.HTTP_204_NO_CONTENT)
async def message_all(message: Message, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    background_tasks.add_task(send_messages, message, db)
    return {}


def send_messages(message: Message, db: Session):
    users = crud.get_users_all(db)
    for user in users:
        print(f"Sending message {message.content} to {user.id}")


print(celery)