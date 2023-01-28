from pydantic import BaseModel, EmailStr


class teacher_create(BaseModel):
    email:EmailStr
    password:str
    name:str
    modulus:list[int]
    
class teacher_dto(teacher_create):

    id:int
    class Config: 
        orm_mode=True

