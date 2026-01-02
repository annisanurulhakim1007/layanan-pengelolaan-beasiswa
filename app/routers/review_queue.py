from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import Application
from ..schemas.application import ApplicationRead, ApplicationStatus

router = APIRouter(prefix="/review-queue", tags=["Review Queue"])

@router.get("/", response_model=List[ApplicationRead])
def get_review_queue(
    status: Optional[ApplicationStatus] = ApplicationStatus.PENDING,
    db: Session = Depends(get_db)
):
    """
    Antrian pengajuan untuk diverifikasi (default: PENDING).
    Ini bukan tabel baru, hanya query dari applications.
    """
    q = db.query(Application)
    if status:
        q = q.filter(Application.current_status == status.value)
    return q.order_by(Application.created_at.asc()).all()
