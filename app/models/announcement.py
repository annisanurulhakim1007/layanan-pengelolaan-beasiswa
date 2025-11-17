# app/models/announcement.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from datetime import datetime
from ..database import Base

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    scholarship_type_id = Column(Integer, ForeignKey("scholarship_types.id"), nullable=True)
    scholarship_period_id = Column(Integer, ForeignKey("scholarship_periods.id"), nullable=True)
    published_at = Column(DateTime, default=datetime.utcnow)
    is_published = Column(Boolean, default=False)
