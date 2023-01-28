from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, Table, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class_modulus = Table(
    "class_modulus",
    Base.metadata,
    Column("class_id", ForeignKey("classes.id"),primary_key=True),
    Column("modulus_id", ForeignKey("modulus.id"),primary_key=True),
)

class_teacher = Table(
    "class_teacher",
    Base.metadata,
    Column("class_id", ForeignKey("classes.id"),primary_key=True),
    Column("teacher_id", ForeignKey("teachers.id"),primary_key=True),
)


class Class(Base):
    __tablename__="classes"

    id=Column(Integer,primary_key=True,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    modulus = relationship("Modulus", secondary=class_modulus,backref='classes')
    teachers = relationship("Teacher", secondary=class_teacher,backref='teachers')
    student = relationship("Student")
    grade = relationship("Grade")

