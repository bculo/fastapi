from sqlalchemy.orm import Session

from sql import models


def get_all(db: Session):
    return db.query(models.Student).all()

