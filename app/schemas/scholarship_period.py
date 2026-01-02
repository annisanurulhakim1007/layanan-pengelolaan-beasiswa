# app/schemas/scholarship_period.py

from pydantic import BaseModel
from datetime import date
from typing import Optional


class ScholarshipPeriodBase(BaseModel):
    year: int
    term_name: str
    start_date: date
    end_date: date
    is_active: bool = True


class ScholarshipPeriodCreate(ScholarshipPeriodBase):
    pass


class ScholarshipPeriodUpdate(BaseModel):
    year: Optional[int] = None
    term_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_active: Optional[bool] = None


class ScholarshipPeriodOut(ScholarshipPeriodBase):
    id: int

    class Config:
        orm_mode = True
