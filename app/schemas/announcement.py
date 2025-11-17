# app/schemas/announcement.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    scholarship_type_id: Optional[int] = None
    scholarship_period_id: Optional[int] = None


class AnnouncementResponse(BaseModel):
    id: int
    title: str
    content: str
    scholarship_type_id: Optional[int] = None
    scholarship_period_id: Optional[int] = None
    published_at: datetime
    is_published: bool

    class Config:
        orm_mode = True
