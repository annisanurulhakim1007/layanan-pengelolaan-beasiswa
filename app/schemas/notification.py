# app/schemas/notification.py
from pydantic import BaseModel
from typing import Optional

class NotificationRead(BaseModel):
    id: int
    student_id: int
    application_id: Optional[int]
    title: str
    message: str
    is_read: bool
    created_at: str

    class Config:
        orm_mode = True
