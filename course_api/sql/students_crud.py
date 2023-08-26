from sqlalchemy.orm import Session

from sql import models


def get_all(db: Session) -> list[models.Student]:
    return db.query(models.Student).all()


def create(db: Session, new_student: models.Student) -> int:
    db.add(new_student)
    db.commit()
    return new_student.id

