from pydantic import BaseModel, EmailStr


class student_create(BaseModel):
    email:EmailStr
    password:str
    name:str
    class_id:int
    
class student_dto(student_create):

    id:int
    class Config: 
        orm_mode=True

