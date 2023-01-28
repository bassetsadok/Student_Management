from pydantic import BaseModel, EmailStr


class modulus_create(BaseModel):
    name:str
    
class modulus_dto(modulus_create):

    id:int
    class Config: 
        orm_mode=True

