# app/models/scholarship.py
from sqlalchemy import Column, Integer, String, Boolean, Text, Date, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from ..database import Base

class ScholarshipType(Base):
    __tablename__ = "scholarship_types"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean, default=True)

    applications = relationship("Application", back_populates="scholarship_type")


class ScholarshipPeriod(Base):
    __tablename__ = "scholarship_periods"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    term_name = Column(String(50), nullable=False)  # "Gelombang 1"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)

    applications = relationship("Application", back_populates="scholarship_period")


class ScholarshipRequirement(Base):
    __tablename__ = "scholarship_requirements"

    id = Column(Integer, primary_key=True, index=True)
    scholarship_type_id = Column(Integer, ForeignKey("scholarship_types.id"), nullable=False)
    scholarship_period_id = Column(Integer, ForeignKey("scholarship_periods.id"), nullable=True)
    min_gpa = Column(Numeric(3, 2))
    min_semester = Column(Integer)
    required_documents = Column(Text)   # misal: "KHS, Surat Keterangan Tidak Mampu"
    other_conditions = Column(Text)

    scholarship_type = relationship("ScholarshipType")
    scholarship_period = relationship("ScholarshipPeriod")
