# app/schemas/application.py
from typing import Optional
from decimal import Decimal
from enum import Enum
from datetime import datetime

from pydantic import BaseModel, Field


class ApplicationStatus(str, Enum):
    """
    Status yang merepresentasikan tahap pengajuan beasiswa.
    """
    PENDING = "PENDING"      # Baru diajukan, menunggu verifikasi
    VERIFIED = "VERIFIED"    # Sudah diverifikasi admin
    ACCEPTED = "ACCEPTED"    # Dinyatakan lolos / diterima
    REJECTED = "REJECTED"    # Ditolak


# =========================
# APPLICATION
# =========================

class ApplicationCreate(BaseModel):
    student_id: int = Field(
        ...,
        description="ID mahasiswa yang mengajukan beasiswa.",
        example=12345,
    )
    scholarship_type_id: int = Field(
        ...,
        description="ID jenis beasiswa yang diajukan.",
        example=1,
    )
    scholarship_period_id: int = Field(
        ...,
        description="ID periode beasiswa yang sedang dibuka.",
        example=2,
    )
    gpa: Decimal = Field(
        ...,
        description="IPK terakhir mahasiswa.",
        example="3.75",
    )
    semester: int = Field(
        ...,
        description="Semester aktif mahasiswa saat mengajukan.",
        example=5,
    )
    reason: str = Field(
        ...,
        description="Alasan atau motivasi pengajuan beasiswa.",
        example="Membantu meringankan biaya kuliah karena kondisi ekonomi keluarga.",
    )


class ApplicationRead(BaseModel):
    id: int = Field(
        ...,
        description="ID unik pengajuan beasiswa.",
        example=10,
    )
    student_id: int = Field(
        ...,
        description="ID mahasiswa yang mengajukan beasiswa.",
        example=12345,
    )
    scholarship_type_id: int = Field(
        ...,
        description="ID jenis beasiswa yang diajukan.",
        example=1,
    )
    scholarship_period_id: int = Field(
        ...,
        description="ID periode beasiswa.",
        example=2,
    )
    gpa: Decimal = Field(
        ...,
        description="IPK terakhir mahasiswa.",
        example="3.75",
    )
    semester: int = Field(
        ...,
        description="Semester aktif mahasiswa.",
        example=5,
    )
    reason: str = Field(
        ...,
        description="Alasan atau motivasi pengajuan beasiswa.",
        example="Membantu meringankan biaya kuliah karena kondisi ekonomi keluarga.",
    )
    current_status: ApplicationStatus = Field(
        ...,
        description="Status pengajuan saat ini.",
        example=ApplicationStatus.PENDING,
    )

    class Config:
        orm_mode = True  # kalau pakai Pydantic v2 bisa diganti from_attributes = True


# =========================
# DOCUMENTS
# =========================

class ApplicationDocumentCreate(BaseModel):
    document_type: str = Field(
        ...,
        description="Jenis dokumen pendukung yang diunggah.",
        example="KHS",
    )
    file_name: str = Field(
        ...,
        description="Nama file asli atau nama file yang disimpan.",
        example="khs_semester_5.pdf",
    )
    file_path: str = Field(
        ...,
        description="Path atau URL file yang sudah tersimpan di server / storage.",
        example="/uploads/documents/12345/khs_semester_5.pdf",
    )


class ApplicationDocumentRead(BaseModel):
    id: int = Field(
        ...,
        description="ID unik dokumen pengajuan.",
        example=7,
    )
    document_type: str = Field(
        ...,
        description="Jenis dokumen pendukung.",
        example="KHS",
    )
    file_name: str = Field(
        ...,
        description="Nama file dokumen.",
        example="khs_semester_5.pdf",
    )
    file_path: str = Field(
        ...,
        description="Path atau URL file dokumen yang dapat diakses.",
        example="/uploads/documents/12345/khs_semester_5.pdf",
    )

    class Config:
        orm_mode = True


# =========================
# STATUS HISTORY
# =========================

class ApplicationStatusHistoryRead(BaseModel):
    id: int = Field(
        ...,
        description="ID unik riwayat perubahan status.",
        example=20,
    )
    old_status: Optional[ApplicationStatus] = Field(
        None,
        description="Status pengajuan sebelum perubahan. Bisa kosong jika ini status pertama.",
        example=ApplicationStatus.PENDING,
    )
    new_status: ApplicationStatus = Field(
        ...,
        description="Status baru yang diberikan pada pengajuan.",
        example=ApplicationStatus.VERIFIED,
    )
    note: Optional[str] = Field(
        None,
        description="Catatan tambahan terkait perubahan status.",
        example="Dokumen sudah lengkap dan sesuai persyaratan.",
    )

    class Config:
        orm_mode = True
