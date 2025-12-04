from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.application import Application, ApplicationStatus

router = APIRouter(prefix="/review-queue", tags=["Review Queue"])

@router.get("/")
def get_review_queue(db: Session = Depends(get_db)):
    # Ambil semua aplikasi dengan status PENDING
    pending_apps = db.query(Application).filter(
        Application.current_status == ApplicationStatus.PENDING
    ).all()

    return {
        "count": len(pending_apps),
        "items": pending_apps
    }
