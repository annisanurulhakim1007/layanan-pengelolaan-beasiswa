# app/schemas/student.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


class StudentProfileBase(BaseModel):
    nim: str
    full_name: str
    study_program: Optional[str] = None
    semester: Optional[int] = None
    gpa: Optional[Decimal] = None
    phone: Optional[str] = None
    address: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    pass


class StudentProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    study_program: Optional[str] = None
    semester: Optional[int] = None
    gpa: Optional[Decimal] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class StudentProfileOut(StudentProfileBase):
    id: int

    class Config:
        from_attributes = True  # Pydantic v2
