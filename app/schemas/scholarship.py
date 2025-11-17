# app/schemas/scholarship.py
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ScholarshipTypeRead(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


class ScholarshipPeriodRead(BaseModel):
    id: int
    year: int
    term_name: str
    start_date: str   # bisa juga date
    end_date: str
    is_active: bool

    class Config:
        orm_mode = True


class ScholarshipRequirementRead(BaseModel):
    id: int
    scholarship_type_id: int
    scholarship_period_id: Optional[int]
    min_gpa: Optional[Decimal]
    min_semester: Optional[int]
    required_documents: Optional[str]
    other_conditions: Optional[str]

    class Config:
        orm_mode = True
