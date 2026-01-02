from pydantic import BaseModel
from typing import Optional

class NotificationCreate(BaseModel):
    student_id: int
    application_id: Optional[int] = None
    title: str
    message: str

class NotificationRead(BaseModel):
    id: int
    student_id: int
    application_id: Optional[int]
    title: str
    message: str
    is_read: bool

    class Config:
        orm_mode = True
