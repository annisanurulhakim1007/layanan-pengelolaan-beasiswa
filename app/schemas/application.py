# app/schemas/application.py
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


class ApplicationStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class ApplicationCreate(BaseModel):
    student_id: int
    scholarship_type_id: int
    scholarship_period_id: int
    gpa: float
    semester: int
    reason: str


class ApplicationResponse(BaseModel):
    id: int
    student_id: int
    scholarship_type_id: int
    scholarship_period_id: int
    gpa: float
    semester: int
    reason: str
    current_status: ApplicationStatus
    created_at: datetime

    class Config:
        orm_mode = True


class ApplicationDocumentCreate(BaseModel):
    document_type: str
    # file sendiri di-handle sebagai UploadFile di router, di schema cukup info metadata


class ApplicationDocumentResponse(BaseModel):
    id: int
    application_id: int
    document_type: str
    file_name: str
    file_path: str
    uploaded_at: datetime

    class Config:
        orm_mode = True


class ApplicationStatusHistoryResponse(BaseModel):
    id: int
    application_id: int
    old_status: Optional[ApplicationStatus]
    new_status: ApplicationStatus
    changed_by: Optional[int]
    note: Optional[str]
    changed_at: datetime

    class Config:
        orm_mode = True
