# app/schemas/auth.py
from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True
