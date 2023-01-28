from pydantic import BaseModel, EmailStr


class Teacher_create(BaseModel):
    email:EmailStr
    password:str
    name:str
    modulus:list[int]
    
class Teacher_dto(Teacher_create):

    id:int
    class Config: 
        orm_mode=True

