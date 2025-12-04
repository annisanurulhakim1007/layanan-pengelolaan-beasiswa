from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.application import Application, ApplicationStatus

router = APIRouter(prefix="/dashboard-metrics", tags=["Dashboard"])

@router.get("/")
def dashboard_metrics(db: Session = Depends(get_db)):
    total = db.query(Application).count()
    pending = db.query(Application).filter(Application.current_status == ApplicationStatus.PENDING).count()
    verified = db.query(Application).filter(Application.current_status == ApplicationStatus.VERIFIED).count()
    accepted = db.query(Application).filter(Application.current_status == ApplicationStatus.ACCEPTED).count()
    rejected = db.query(Application).filter(Application.current_status == ApplicationStatus.REJECTED).count()

    return {
        "total_applications": total,
        "pending": pending,
        "verified": verified,
        "accepted": accepted,
        "rejected": rejected
    }
