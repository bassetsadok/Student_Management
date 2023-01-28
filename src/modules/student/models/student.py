from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class Student(Base):
    __tablename__="students"

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    name=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    class_id = Column(Integer, ForeignKey('classes.id',ondelete='CASCADE'),nullable=True)
    grade = relationship("Grade")

