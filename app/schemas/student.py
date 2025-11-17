# app/schemas/student.py
from pydantic import BaseModel
from typing import Optional

class StudentBase(BaseModel):
    nim: str
    name: str
    study_program: Optional[str] = None
    semester: Optional[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int

    class Config:
        orm_mode = True
