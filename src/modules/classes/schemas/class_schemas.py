from pydantic import BaseModel, EmailStr


class class_create(BaseModel):
    name:str
    
class class_dto(class_create):

    id:int
    class Config: 
        orm_mode=True

