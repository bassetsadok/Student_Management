from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, Table, text
from sqlalchemy.orm import relationship

from ....db.database import Base

teacher_modulus = Table(
    "teacher_modulus",
    Base.metadata,
    Column("teacher_id", ForeignKey("teachers.id"),primary_key=True),
    Column("modulus_id", ForeignKey("modulus.id"),primary_key=True),
)


class Teacher(Base):
    __tablename__="teachers"

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    name=Column(String,nullable=False)
    modulus = relationship("Modulus", secondary=teacher_modulus,backref='teachers')
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

