from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.modules.grade.models.grade import Grade
from src.modules.grade.models.medium import Medium
from src.modules.grade.schemas.grade_schemas import grade_dto
from src.modules.grade.schemas.medium_schemas import medium_dto

from src.modules.student.schemas.student_schemas import student_create,student_dto
from ....db.database import get_db
from ....auth.token_schemas import Token
from ....auth.oauth2 import create_access_token
from ..models.student import Student
from ....utilities import utils
router= APIRouter(tags=["student"])

@router.post('/login',response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    user=db.query(Student).filter(Student.email== user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credenials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credenials")

    access_token=create_access_token(data={"user_id":user.id})

    return {"token":access_token,"token_type":"bearer"}

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=student_dto)
def create_student(student:student_create,db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password=utils.hash(student.password)
    student.password=hashed_password
    new_student=Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/",response_model=List[student_dto])
async def get_students(db: Session = Depends(get_db)):

    students=db.query(Student).all()
    return students

@router.get('/{id}',response_model=student_dto)
def get_student(id:int,db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == id ).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with id: {id} does not exist")
    
    return student

@router.get('grades/{id}',response_model=List[grade_dto])
def get_student_grades(id:int,db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.student_id == id ).all()
    if not grades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Grades not available")
    
    return grades

@router.get('student_module_grades/{student_id}/{module_id}',response_model=List[grade_dto])
def get_module_grades(student_id:int,module_id:int,db: Session = Depends(get_db)):
    grade = db.query(Grade).filter(Grade.student_id == student_id & Grade.modulus_id == module_id).first()
    if not grade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Grade not available")
    
    return grade

@router.get('student_medium/{student_id}',response_model=medium_dto)
def get_classe_medium(student_id:int,db: Session = Depends(get_db)):
    medium = db.query(Medium).filter(Medium.student_id == student_id).first()
    if not medium:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medium not available")
    
    return medium
