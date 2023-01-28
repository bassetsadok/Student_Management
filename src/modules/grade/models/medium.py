from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class Medium(Base):
    __tablename__="mediums"

    id=Column(Integer,primary_key=True,nullable=False)
    medium=Column(Float,nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    student_id = Column(Integer, ForeignKey('students.id',ondelete='SET NULL'),nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id',ondelete='SET NULL'),nullable=False)

