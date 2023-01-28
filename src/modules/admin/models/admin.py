from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer,Float, String, Table, text
from sqlalchemy.orm import relationship

from ....db.database import Base

class Admin(Base):
    __tablename__="admins"

    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    admin=Column(Boolean)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

