# app/routers/student_applications.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..models.application import Application
from ..schemas.application import ApplicationRead

router = APIRouter(
    prefix="/student-applications",
    tags=["Student Applications"],
)


@router.get(
    "/{student_id}",
    response_model=List[ApplicationRead],
    summary="Ambil semua pengajuan milik satu mahasiswa",
    description=(
        "Mengambil seluruh pengajuan beasiswa yang dimiliki oleh satu mahasiswa tertentu "
        "berdasarkan `student_id`.\n\n"
        "Endpoint ini biasanya digunakan oleh admin untuk melihat riwayat pengajuan beasiswa "
        "seorang mahasiswa."
    ),
    responses={
        200: {"description": "Daftar pengajuan berhasil diambil."},
        404: {"description": "Mahasiswa dengan ID tersebut tidak ditemukan."},
    },
)
def get_applications_by_student(
    student_id: int,
    db: Session = Depends(get_db),
):
    """
    Langkah yang dilakukan endpoint ini:
    1. Cek apakah mahasiswa dengan `student_id` tersebut ada di tabel `students`.
    2. Jika tidak ada → kembalikan HTTP 404 `Student not found`.
    3. Jika ada → ambil semua baris dari tabel `applications` yang memiliki `student_id` tersebut.
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    apps = db.query(Application).filter(Application.student_id == student_id).all()
    return apps
