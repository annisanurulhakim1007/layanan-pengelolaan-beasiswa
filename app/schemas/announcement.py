# app/schemas/announcement.py
from pydantic import BaseModel
from typing import Optional

class AnnouncementRead(BaseModel):
    id: int
    title: str
    content: str
    scholarship_type_id: Optional[int]
    scholarship_period_id: Optional[int]
    published_at: Optional[str]
    is_published: bool

    class Config:
        orm_mode = True
