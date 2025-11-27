# app/schemas/student.py
from typing import Optional
from pydantic import BaseModel, Field


class StudentBase(BaseModel):
    nim: str = Field(
        ...,
        description="Nomor Induk Mahasiswa (NIM) yang digunakan sebagai identitas utama mahasiswa.",
        example="2211521007",
    )
    name: str = Field(
        ...,
        description="Nama lengkap mahasiswa sesuai data akademik.",
        example="Annisa Nurul Hakim",
    )
    study_program: Optional[str] = Field(
        None,
        description="Program studi atau jurusan mahasiswa.",
        example="Sistem Informasi",
    )
    semester: Optional[int] = Field(
        None,
        description="Semester aktif mahasiswa saat ini.",
        example=7,
    )
    email: Optional[str] = Field(
        None,
        description="Alamat email resmi yang digunakan untuk komunikasi akademik.",
        example="2211521007@student.univ.ac.id",
    )
    phone: Optional[str] = Field(
        None,
        description="Nomor telepon / WhatsApp yang dapat dihubungi.",
        example="081234567890",
    )


class StudentCreate(StudentBase):
    """
    Schema untuk pembuatan data mahasiswa baru oleh admin.
    Menggunakan seluruh field dari StudentBase.
    """
    pass


class StudentRead(StudentBase):
    id: int = Field(
        ...,
        description="ID unik mahasiswa di dalam sistem (primary key di database).",
        example=1,
    )

    class Config:
        orm_mode = True
