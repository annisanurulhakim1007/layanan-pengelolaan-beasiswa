# app/models/application.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
    Numeric,
)
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base
import enum


class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    scholarship_type_id = Column(Integer, ForeignKey("scholarship_types.id"), nullable=False)
    scholarship_period_id = Column(Integer, ForeignKey("scholarship_periods.id"), nullable=False)

    gpa = Column(Numeric(3, 2))
    semester = Column(Integer)
    reason = Column(String)

    current_status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False,
    )

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    # relationships (opsional untuk join)
    student = relationship("Student")
    scholarship_type = relationship("ScholarshipType")
    scholarship_period = relationship("ScholarshipPeriod")


class ApplicationDocument(Base):
    __tablename__ = "application_documents"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    document_type = Column(String(50))  # KHS, SURAT_KEMAMPUAN, dll
    file_name = Column(String(200))
    file_path = Column(String(255))
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class ApplicationStatusHistory(Base):
    __tablename__ = "application_status_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    old_status = Column(Enum(ApplicationStatus), nullable=True)
    new_status = Column(Enum(ApplicationStatus), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"))
    note = Column(String)

    changed_at = Column(DateTime, default=datetime.utcnow)
