# app/schemas/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List

# ---------------- Application read (dipakai di review queue)
class ApplicationRead(BaseModel):
    id: int
    student_id: int
    scholarship_type_id: int
    scholarship_period_id: int
    gpa: Optional[float] = None
    semester: Optional[int] = None
    reason: Optional[str] = None
    current_status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True

# ---------------- Decision response
class DecisionRequest(BaseModel):
    decision: str = Field(..., example="approved")  # approved / rejected

class DecisionResponse(BaseModel):
    application_id: int
    new_status: str

# ---------------- Announcement create/read
class AnnouncementCreate(BaseModel):
    title: str = Field(..., example="Pengumuman Hasil Seleksi Beasiswa")
    content: str = Field(..., example="Selamat kepada mahasiswa...")

class AnnouncementRead(BaseModel):
    id: int
    title: str
    content: str
    is_published: Optional[bool] = False
    published_at: Optional[str] = None

    class Config:
        orm_mode = True

# ---------------- Notification read
class NotificationRead(BaseModel):
    id: int
    student_id: int
    application_id: Optional[int] = None
    title: str
    message: str
    is_read: bool
    created_at: Optional[str] = None

    class Config:
        orm_mode = True

# ---------------- Dashboard metrics
class DashboardMetrics(BaseModel):
    total_applications: int
    pending: int
    verified: int
    accepted: int
    rejected: int
