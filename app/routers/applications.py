# app/routers/applications.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..models.application import Application
from ..schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatus,  # enum yang sudah kamu definisikan di schemas/application.py
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "/",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Buat pengajuan beasiswa baru",
    description=(
        "Membuat pengajuan beasiswa baru (Application).\n\n"
        "- Memastikan `student_id` valid (mahasiswa ada di tabel `students`).\n"
        "- Menyimpan pengajuan dengan status awal `PENDING` (di level model/database).\n"
    ),
    responses={
        201: {"description": "Pengajuan beasiswa berhasil dibuat."},
        404: {"description": "Mahasiswa dengan student_id tersebut tidak ditemukan."},
    },
)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
):
    """
    Endpoint ini digunakan untuk admin atau sistem yang ingin mencatat pengajuan beasiswa
    berdasarkan data mahasiswa dan informasi beasiswa yang dia pilih.
    """
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    app_obj = Application(
        student_id=payload.student_id,
        scholarship_type_id=payload.scholarship_type_id,
        scholarship_period_id=payload.scholarship_period_id,
        gpa=payload.gpa,
        semester=payload.semester,
        reason=payload.reason,
        # current_status biasanya di-set default = PENDING di model/database
    )
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj


@router.get(
    "/",
    response_model=List[ApplicationRead],
    summary="List semua pengajuan beasiswa",
    description=(
        "Mengambil daftar semua pengajuan beasiswa yang tersimpan di sistem.\n\n"
        "- Dapat difilter berdasarkan `status` pengajuan (`PENDING`, `VERIFIED`, `ACCEPTED`, `REJECTED`).\n"
        "- Jika parameter `status` tidak diisi, semua pengajuan akan ditampilkan."
    ),
    responses={
        200: {"description": "Daftar pengajuan berhasil diambil."},
    },
)
def list_applications(
    status_filter: Optional[ApplicationStatus] = Query(
        default=None,
        alias="status",
        description=(
            "Filter opsional berdasarkan status pengajuan.\n\n"
            "Nilai yang diperbolehkan: `PENDING`, `VERIFIED`, `ACCEPTED`, `REJECTED`."
        ),
        example="PENDING",
    ),
    db: Session = Depends(get_db),
):
    """
    Mengambil daftar pengajuan dari tabel `applications`, dengan opsi filter berdasarkan status.
    """
    query = db.query(Application)
    if status_filter:
        query = query.filter(Application.current_status == status_filter)
    apps = query.all()
    return apps


@router.get(
    "/{application_id}",
    response_model=ApplicationRead,
    summary="Ambil detail pengajuan berdasarkan ID",
    description="Mengambil detail lengkap satu pengajuan beasiswa berdasarkan `application_id`.",
    responses={
        200: {"description": "Detail pengajuan ditemukan dan dikembalikan."},
        404: {"description": "Pengajuan dengan ID tersebut tidak ditemukan."},
    },
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Endpoint ini biasa dipakai oleh admin atau sistem untuk melihat detail satu pengajuan,
    misalnya saat proses verifikasi atau penilaian.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj
