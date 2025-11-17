# app/schemas/application.py
from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ApplicationCreate(BaseModel):
    student_id: int
    scholarship_type_id: int
    scholarship_period_id: int
    gpa: Decimal
    semester: int
    reason: str


class ApplicationRead(BaseModel):
    id: int
    student_id: int
    scholarship_type_id: int
    scholarship_period_id: int
    gpa: Decimal
    semester: int
    reason: str
    current_status: ApplicationStatus

    class Config:
        orm_mode = True


class ApplicationDocumentCreate(BaseModel):
    document_type: str
    file_name: str
    file_path: str


class ApplicationDocumentRead(BaseModel):
    id: int
    document_type: str
    file_name: str
    file_path: str

    class Config:
        orm_mode = True


class ApplicationStatusHistoryRead(BaseModel):
    id: int
    old_status: Optional[ApplicationStatus]
    new_status: ApplicationStatus
    note: Optional[str]

    class Config:
        orm_mode = True
