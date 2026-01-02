from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import Application, ApplicationStatusHistory, ApplicationStatus
from ..models.student import Student
from ..models.notification import Notification
from ..schemas.application import ApplicationRead

router = APIRouter(prefix="/decisions", tags=["Decisions (Admin)"])

class DecisionRequest(BaseModel):
    decision: str  # "ACCEPTED" atau "REJECTED"
    note: Optional[str] = None

@router.post("/{application_id}", response_model=ApplicationRead, status_code=status.HTTP_200_OK)
def decide_application(application_id: int, payload: DecisionRequest, db: Session = Depends(get_db)):
    """
    Keputusan akhir admin:
    - Update applications.current_status
    - Insert application_status_history
    - Create notifications untuk mahasiswa terkait
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    decision_upper = payload.decision.strip().upper()
    if decision_upper not in ["ACCEPTED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Decision must be ACCEPTED or REJECTED")

    old_status = app_obj.current_status
    new_status = ApplicationStatus(decision_upper)

    # update status aplikasi
    app_obj.current_status = new_status

    # tulis history
    history = ApplicationStatusHistory(
        application_id=application_id,
        old_status=old_status,
        new_status=new_status,
        changed_by=None,  # kamu belum pakai auth, jadi null
        note=payload.note
    )
    db.add(history)

    # buat notifikasi
    notif_title = "Hasil Pengajuan Beasiswa"
    notif_msg = (
        f"Pengajuan beasiswa kamu #{application_id} dinyatakan {decision_upper}."
        + (f" Catatan: {payload.note}" if payload.note else "")
    )

    notif = Notification(
        student_id=app_obj.student_id,
        application_id=application_id,
        title=notif_title,
        message=notif_msg
    )
    db.add(notif)

    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj
