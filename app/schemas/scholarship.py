# app/schemas/scholarship.py
from pydantic import BaseModel
from typing import Optional
from datetime import date


class ScholarshipTypeResponse(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


class ScholarshipPeriodResponse(BaseModel):
    id: int
    year: int
    term_name: str
    start_date: date
    end_date: date
    is_active: bool

    class Config:
        orm_mode = True


class ScholarshipRequirementResponse(BaseModel):
    id: int
    scholarship_type_id: int
    scholarship_period_id: Optional[int] = None
    min_gpa: Optional[str] = None
    min_semester: Optional[int] = None
    required_documents: Optional[str] = None
    other_conditions: Optional[str] = None

    class Config:
        orm_mode = True
