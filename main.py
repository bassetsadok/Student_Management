from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from src.db import  database
import os
from dotenv import load_dotenv
from src.utilities.utils import create_admin
from src.modules.modulus.models import modulus
from src.modules.teacher.models import teacher
from src.modules.classes.models import classes
from src.modules.student.models import student
from src.modules.grade.models import grade,medium

from src.modules.modulus.routes import modulus_routes
from src.modules.classes.routes import class_routes
from src.modules.grade.routes import grade_routes
from src.modules.student.routes import student_routes
from src.modules.teacher.routes import teacher_routes

load_dotenv()  

modulus.Base.metadata.create_all(bind=database.engine)
medium.Base.metadata.create_all(bind=database.engine)
teacher.Base.metadata.create_all(bind=database.engine)
classes.Base.metadata.create_all(bind=database.engine)
student.Base.metadata.create_all(bind=database.engine)
grade.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

while True:
    try:
        conn=psycopg2.connect(host=os.getenv("HOST"),database=os.getenv("DATABASE"),user=os.getenv("USER"),password=os.getenv("PASSWORD"),cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("database connection was successfull ✅")
        create_admin()
        break
    except Exception as error:
        print("connection to database was failed")
        print("error was ",error)
        time.sleep(3)

app.include_router(modulus_routes.router)
app.include_router(class_routes.router)
app.include_router(grade_routes.router)
app.include_router(student_routes.router)
app.include_router(teacher_routes.router)

@app.get("/")
async def root():
    print(os.getenv("DOMAIN"))
    return {"message":"hello basset hey" }
