# app/models/application.py
from sqlalchemy import Column, Integer, Numeric, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
from .application_status_enum import ApplicationStatus

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    scholarship_type_id = Column(Integer, ForeignKey("scholarship_types.id"), nullable=False)
    scholarship_period_id = Column(Integer, ForeignKey("scholarship_periods.id"), nullable=False)
    gpa = Column(Numeric(3, 2))
    semester = Column(Integer)
    reason = Column(Text)
    current_status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student")
    scholarship_type = relationship("ScholarshipType", back_populates="applications")
    scholarship_period = relationship("ScholarshipPeriod", back_populates="applications")
    documents = relationship("ApplicationDocument", back_populates="application")
    status_history = relationship("ApplicationStatusHistory", back_populates="application")


class ApplicationDocument(Base):
    __tablename__ = "application_documents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    document_type = Column(String(50))      # KHS, SURAT_PENDUKUNG, dll
    file_name = Column(String(200))
    file_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="documents")


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    old_status = Column(Enum(ApplicationStatus), nullable=True)
    new_status = Column(Enum(ApplicationStatus), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # admin
    note = Column(Text)
    changed_at = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="status_history")
