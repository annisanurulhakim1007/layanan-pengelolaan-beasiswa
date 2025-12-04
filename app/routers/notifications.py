from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notification import Notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/{student_id}")
def get_notifications(student_id: int, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(
        Notification.student_id == student_id
    ).order_by(Notification.created_at.desc()).all()

    return {
        "count": len(notifications),
        "items": notifications
    }
