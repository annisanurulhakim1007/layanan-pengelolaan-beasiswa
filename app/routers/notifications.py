from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.notification import Notification
from ..models.student import Student
from ..schemas.notification import NotificationCreate, NotificationRead

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
def create_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    # validasi student
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    notif = Notification(
        student_id=payload.student_id,
        application_id=payload.application_id,
        title=payload.title,
        message=payload.message
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

@router.get("/students/{student_id}", response_model=List[NotificationRead])
def list_notifications_by_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return (
        db.query(Notification)
        .filter(Notification.student_id == student_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_notification_read(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(Notification).filter(Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")

    notif.is_read = True
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif
