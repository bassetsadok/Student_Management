from pydantic import BaseModel

class grade_create(BaseModel):
    grade:float
    student_id:int
    modulus_id:int
    class_id:int

class grade_dto(grade_create):
    id:int
    class Config: 
        orm_mode=True
