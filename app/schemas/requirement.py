# app/schemas/requirement.py
from pydantic import BaseModel
from typing import Optional


class RequirementBase(BaseModel):
    scholarship_type_id: int
    scholarship_period_id: Optional[int] = None
    min_gpa: Optional[float] = None
    min_semester: Optional[int] = None
    required_documents: Optional[str] = None
    other_conditions: Optional[str] = None


class RequirementCreate(RequirementBase):
    pass


class RequirementUpdate(BaseModel):
    scholarship_type_id: Optional[int] = None
    scholarship_period_id: Optional[int] = None
    min_gpa: Optional[float] = None
    min_semester: Optional[int] = None
    required_documents: Optional[str] = None
    other_conditions: Optional[str] = None


class RequirementOut(RequirementBase):
    id: int

    class Config:
        orm_mode = True
