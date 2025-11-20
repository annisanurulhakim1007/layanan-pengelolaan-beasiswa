from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import Application, ApplicationStatusHistory
from ..schemas.application import ApplicationStatusHistoryRead

router = APIRouter(
    prefix="/status-history",
    tags=["Status History"],
)


@router.get("/{application_id}", response_model=List[ApplicationStatusHistoryRead])
def get_status_history(application_id: int, db: Session = Depends(get_db)):
    """
    Mengambil riwayat perubahan status untuk satu pengajuan.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    history = (
        db.query(ApplicationStatusHistory)
        .filter(ApplicationStatusHistory.application_id == application_id)
        .order_by(ApplicationStatusHistory.changed_at.asc())
        .all()
    )

    return history
