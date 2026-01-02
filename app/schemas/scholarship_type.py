# app/schemas/scholarship_type.py
from pydantic import BaseModel
from typing import Optional

class ScholarshipTypeBase(BaseModel):
    code: str
    name: str
    description: str | None = None
    is_active: bool = True

class ScholarshipTypeCreate(ScholarshipTypeBase):
    pass

class ScholarshipTypeUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: bool | None = None

class ScholarshipTypeOut(ScholarshipTypeBase):
    id: int

    class Config:
        orm_mode = True  # Pydantic v2
