from fastapi import APIRouter, Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.modules.modulus.schemas.modulus_schemas import modulus_create, modulus_dto
from typing import List
from src.modules.teacher.schemas.teacher_schemas import Teacher_create
from ....db.database import get_db
from ....auth.token_schemas import Token
from ....auth.oauth2 import get_current_user
from ..models.modulus import Modulus
from ....utilities import utils

router= APIRouter(tags=["modulus"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=modulus_dto)
async def create_modulus(modulus:modulus_create,db: Session = Depends(get_db),current_user=Depends(get_current_user)):
    if not current_user.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not autherized to perform requested action")

    new_modulus=Modulus(**modulus.dict())
    db.add(new_modulus)
    db.commit()
    db.refresh(new_modulus)

    return new_modulus

@router.get("/",response_model=List[modulus_dto])
async def get_modulus(db: Session = Depends(get_db)):

    modulus=db.query(Modulus).all()
    return modulus

@router.get('/{id}',response_model=modulus_dto)
def get_modulus(id:int,db: Session = Depends(get_db)):
    modulus = db.query(Modulus).filter(Modulus.id == id ).first()
    if not modulus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Modulus with id: {id} does not exist")
    
    return modulus
