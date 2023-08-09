from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from domain.exceptions import NotFoundException, CoreException

from sql import crud, models, schemas
from sql.database import engine, SessionLocal
from sql.dependencies import get_db

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
    models = []
    for user in users:
        models.append(schemas.User(**user.__dict__))
    return models


@router.get("/me")
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}")
async def read_user(username: str):
    return {"username": username}

