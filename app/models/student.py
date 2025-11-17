# app/models/student.py
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from ..database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    nim = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    study_program = Column(String(100))
    semester = Column(Integer)
    email = Column(String(100))
    phone = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)
