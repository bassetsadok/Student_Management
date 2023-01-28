from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.modules.classes.models.classes import Class
from src.modules.grade.models.medium import Medium
from src.modules.grade.schemas.grade_schemas import grade_create,grade_dto
from src.modules.student.models.student import Student
from ....db.database import get_db
from ....auth.token_schemas import Token
from ....auth.oauth2 import create_access_token
from ..models.grade import Grade
from ....utilities import utils
router= APIRouter(tags=["grade"])

@router.post("/add_student_grade",status_code=status.HTTP_201_CREATED)
def add_student_grade(grade:grade_create,db: Session = Depends(get_db)):
    # if not current_user.admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_grade=Grade(**grade.dict())
    db.add(new_grade)
    db.commit()
    db.refresh(new_grade)

    return new_grade

@router.get('/{module_id}',response_model=List[grade_dto])
def get_module_grades(module_id:int,db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.id == module_id ).all()
    if not grades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Module with id: {id} does not exist")
    
    return grades

@router.post("/class_medium/{class_id}",status_code=status.HTTP_201_CREATED)
def calculate_class_medium(class_id:int,db: Session = Depends(get_db)):
    # if not current_user.admin:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")
    students = db.query(Student).filter(Student.class_id == class_id ).all()
    classe = db.query(Class).filter(Class.id == class_id ).first()
    modules_length=classe.modulus.length()

    for student in students:
       grades = db.query(Grade).filter(Grade.student_id == student.id ).all()
       student_medium=utils.calculate_medium(grades,modules_length)
       medium=Medium(medium=student_medium,student_id=student.id,class_id=class_id)
       db.add(medium)
       db.commit()
       db.refresh(medium)

    return 
