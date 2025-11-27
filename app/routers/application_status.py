# app/routers/application_status.py
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import (
    Application,
    ApplicationStatus,
    ApplicationStatusHistory,
)
from ..schemas.application import ApplicationRead, ApplicationStatus as SchemaStatus

router = APIRouter(
    prefix="/application-status",
    tags=["Application Status"],
)


class ApplicationStatusUpdate(BaseModel):
    """
    Schema lokal untuk update status aplikasi.
    Dipakai sebagai body untuk endpoint PATCH /application-status/{application_id}.
    """
    new_status: SchemaStatus = Field(
        ...,
        description=(
            "Status baru yang akan diberikan kepada pengajuan. "
            "Nilai yang diperbolehkan: PENDING, VERIFIED, ACCEPTED, REJECTED."
        ),
        example=SchemaStatus.VERIFIED,
    )
    note: Optional[str] = Field(
        None,
        description="Catatan tambahan terkait perubahan status (opsional).",
        example="Semua dokumen sudah lengkap dan valid.",
    )


@router.get(
    "/{application_id}",
    response_model=ApplicationRead,
    summary="Ambil status terkini pengajuan beasiswa",
    description=(
        "Mengambil detail lengkap satu pengajuan beasiswa beserta status terkini "
        "berdasarkan `application_id`.\n\n"
        "Endpoint ini biasanya digunakan oleh admin atau sistem lain untuk mengetahui "
        "posisi terakhir pengajuan dalam proses seleksi."
    ),
    responses={
        200: {"description": "Detail pengajuan dan status saat ini berhasil diambil."},
        404: {"description": "Pengajuan dengan ID tersebut tidak ditemukan."},
    },
)
def get_current_application_status(
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Langkah endpoint ini:
    1. Cek apakah pengajuan dengan `application_id` ada di tabel `applications`.
    2. Jika tidak ada → HTTP 404 `Application not found`.
    3. Jika ada → kembalikan objek aplikasi lengkap (mengandung `current_status`).
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found"
        )
    return app_obj


@router.patch(
    "/{application_id}",
    response_model=ApplicationRead,
    summary="Update status pengajuan & catat ke riwayat",
    description=(
        "Mengubah status terkini suatu pengajuan beasiswa dan otomatis mencatat perubahan "
        "tersebut ke tabel `application_status_history`.\n\n"
        "Perilaku:\n"
        "- Tidak menghapus data lama.\n"
        "- `old_status` diisi dengan status sebelum perubahan.\n"
        "- `new_status` diisi dengan status baru yang dikirim pada body.\n"
        "- `note` bersifat opsional, bisa diisi alasan atau catatan admin."
    ),
    responses={
        200: {"description": "Status pengajuan berhasil diperbarui."},
        400: {"description": "Nilai status yang diberikan tidak valid."},
        404: {"description": "Pengajuan dengan ID tersebut tidak ditemukan."},
    },
)
def update_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Endpoint ini digunakan untuk admin (atau sistem) yang ingin:
    - Mengubah status pengajuan (misalnya dari PENDING → VERIFIED, atau VERIFIED → ACCEPTED).
    - Menjaga jejak audit perubahan melalui tabel `application_status_history`.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Application not found"
        )

    old_status = app_obj.current_status

    # Validasi dan mapping status baru ke model Enum di sisi database
    try:
        new_status_model = ApplicationStatus(payload.new_status.value)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status value"
        )

    # Update status di tabel applications
    app_obj.current_status = new_status_model

    # Catat ke status history
    history = ApplicationStatusHistory(
        application_id=application_id,
        old_status=old_status,
        new_status=new_status_model,
        changed_by=None,  # bisa diisi user_id admin jika nanti ada modul autentikasi
        note=payload.note,
    )

    db.add(app_obj)
    db.add(history)
    db.commit()
    db.refresh(app_obj)
    return app_obj
