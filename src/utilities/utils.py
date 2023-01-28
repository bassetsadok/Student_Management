from fastapi import Depends
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from ..db.database import get_db,engine
from src.modules.admin.models.admin import Admin
from sqlalchemy.orm import Session
from sqlalchemy import insert,select

load_dotenv()  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password:str):
    #hash the password - password
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def create_admin(db: Session = Depends(get_db)):
    email=os.getenv("ADMIN_EMAIL")
    password=os.getenv("ADMIN_PASSWORD")

    admin_existed=select(Admin).where(Admin.email == email)
    with engine.connect() as conn:
        for row in conn.execute(stmt):
            if row:
                return

    #hash the password - user.password
    hashed_password=hash(password)
    
    password=hashed_password
    stmt = insert(Admin).values(email=email,password=password,admin=True)
    # new_admin=Admin(email=email,password=password,admin=True)
    # db.add(new_admin)
    # db.commit()
    # db.refresh(new_admin)

    compiled = stmt.compile()
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

    return compiled

def calculate_medium(grades,length):
    for grade in grades:
        sum =sum+grade
    return sum/length
