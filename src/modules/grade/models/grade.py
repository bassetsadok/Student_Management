from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class Grade(Base):
    __tablename__="grades"

    id=Column(Integer,primary_key=True,nullable=False)
    grade=Column(Float,nullable=True)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    student_id = Column(Integer, ForeignKey('students.id',ondelete='SET NULL'),nullable=False)
    modulus_id = Column(Integer, ForeignKey('modulus.id',ondelete='SET NULL'),nullable=False)
    class_id = Column(Integer, ForeignKey('classes.id',ondelete='SET NULL'),nullable=False)

