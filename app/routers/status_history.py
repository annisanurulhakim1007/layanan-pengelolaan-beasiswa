# app/routers/status_history.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import Application, ApplicationStatusHistory
from ..schemas.application import ApplicationStatusHistoryRead

router = APIRouter(
    prefix="/status-history",
    tags=["Status History"],
)


@router.get(
    "/{application_id}",
    response_model=List[ApplicationStatusHistoryRead],
    summary="Ambil riwayat perubahan status untuk satu pengajuan",
    description=(
        "Mengambil seluruh riwayat perubahan status (`application_status_history`) "
        "untuk satu pengajuan beasiswa berdasarkan `application_id`.\n\n"
        "Catatan:\n"
        "- Endpoint ini hanya bisa diakses jika pengajuan dengan ID tersebut ada.\n"
        "- Hasil dikembalikan dalam urutan kronologis (paling lama di atas, paling baru di bawah)."
    ),
    responses={
        200: {"description": "Riwayat status untuk pengajuan berhasil diambil."},
        404: {"description": "Pengajuan dengan ID tersebut tidak ditemukan."},
    },
)
def get_status_history(
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Langkah kerja endpoint ini:
    1. Cek apakah pengajuan dengan `application_id` ada di tabel `applications`.
    2. Jika tidak ada → HTTP 404 `Application not found`.
    3. Jika ada → ambil semua baris di `application_status_history` milik pengajuan tersebut,
       diurutkan berdasarkan `changed_at` secara ascending (tertua ke terbaru).
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    history = (
        db.query(ApplicationStatusHistory)
        .filter(ApplicationStatusHistory.application_id == application_id)
        .order_by(ApplicationStatusHistory.changed_at.asc())
        .all()
    )

    return history
