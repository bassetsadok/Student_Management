from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.modules.teacher.schemas.teacher_schemas import teacher_create,teacher_dto
from ....db.database import get_db
from ....auth.token_schemas import Token
from ....auth.oauth2 import create_access_token
from ..models.teacher import Teacher
from ....utilities import utils
router= APIRouter(tags=["teacher"])

@router.post('/login',response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):

    user=db.query(Teacher).filter(Teacher.email== user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credenials")
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credenials")

    access_token=create_access_token(data={"user_id":user.id})

    return {"token":access_token,"token_type":"bearer"}

@router.post("/",status_code=status.HTTP_201_CREATED)
def create_teacher(teacher:teacher_create,db: Session = Depends(get_db)):

    #hash the password - user.password
    hashed_password=utils.hash(teacher.password)
    teacher.password=hashed_password
    new_teacher=Teacher(**teacher.dict())
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    return new_teacher

@router.get("/",response_model=List[teacher_dto])
async def get_teachers(db: Session = Depends(get_db)):

    teachers=db.query(Teacher).all()
    return teachers

@router.get('/{id}',response_model=teacher_dto)
def get_teacher(id:int,db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.id == id ).first()
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Teacher with id: {id} does not exist")
    
    return teacher
