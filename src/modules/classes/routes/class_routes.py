from typing import List
from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.modules.classes.models.classes import Class

from src.modules.classes.schemas.class_schemas import class_create,class_dto
from src.modules.grade.models.grade import Grade
from src.modules.grade.schemas.grade_schemas import grade_dto
from src.modules.grade.schemas.medium_schemas import medium_dto
from ....db.database import get_db
from ....auth.token_schemas import Token
from ....auth.oauth2 import create_access_token, get_current_user
router= APIRouter(tags=["class"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=class_dto)
async def create_class(classe:class_create,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_class=Class(**classe.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class

@router.get("/",response_model=List[class_dto])
async def get_class(db: Session = Depends(get_db)):

    classes=db.query(Class).all()
    return classes

@router.get('/{id}',response_model=class_dto)
def get_class(id:int,db: Session = Depends(get_db)):
    classe = db.query(Class).filter(Class.id == id ).first()
    if not classe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Class with id: {id} does not exist")
    
    return classe


@router.get('module_grades/{class_id}/{module_id}',response_model=List[grade_dto])
def get_module_grades(class_id:int,module_id:int,db: Session = Depends(get_db)):
    grades = db.query(Grade).filter(Grade.class_id == class_id & Grade.modulus_id == module_id).all()
    if not grades:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Grades not available")
    
    return grades


@router.get('class_medium/{class_id}',response_model=List[medium_dto])
def get_classe_medium(class_id:int,db: Session = Depends(get_db)):
    mediums = db.query(Grade).filter(Grade.class_id == class_id).all()
    if not mediums:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medium not available")
    
    return mediums
