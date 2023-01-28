from pydantic import BaseModel

class medium_create(BaseModel):
    medium:float
    student_id:int
    modulus_id:int
    class_id:int

class medium_dto(medium_create):
    id:int
    class Config: 
        orm_mode=True
