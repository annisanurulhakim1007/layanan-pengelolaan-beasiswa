from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
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
    """
    new_status: SchemaStatus
    note: Optional[str] = None


@router.get("/{application_id}", response_model=ApplicationRead)
def get_current_application_status(
    application_id: int, db: Session = Depends(get_db)
):
    """
    Mengambil status terkini (beserta detail aplikasi) untuk satu pengajuan.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application_status(
    application_id: int,
    payload: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
):
    """
    Mengubah status aplikasi dan otomatis mencatat ke application_status_history.
    - Tidak menghapus data.
    - Status lama disimpan sebagai old_status.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    old_status = app_obj.current_status

    try:
        new_status_model = ApplicationStatus(payload.new_status.value)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid status value")

    # update status di tabel applications
    app_obj.current_status = new_status_model

    # catat ke status history
    history = ApplicationStatusHistory(
        application_id=application_id,
        old_status=old_status,
        new_status=new_status_model,
        changed_by=None,  # bisa diisi user_id admin jika ada auth
        note=payload.note,
    )

    db.add(app_obj)
    db.add(history)
    db.commit()
    db.refresh(app_obj)
    return app_obj
