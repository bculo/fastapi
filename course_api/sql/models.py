from sqlalchemy import String, ForeignKey, Column, Integer, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
metadata = Base.metadata

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(2000))
    created = Column(DateTime, nullable=False)

    courses = relationship("CourseStudent", back_populates="course")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)

    students = relationship("CourseStudent", back_populates="student")


class CourseStudent(Base):
    __tablename__ = "course_students"

    course_id = Column(Integer, ForeignKey("courses.id"))
    course = relationship("Course", back_populates="courses")
    student_id = Column(Integer, ForeignKey("students.id"))
    student = relationship("Student", back_populates="students")

    __table_args__ = (
        PrimaryKeyConstraint("course_id", "student_id"),
    )






