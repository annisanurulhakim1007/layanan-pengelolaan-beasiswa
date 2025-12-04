from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.application import Application
from app.schemas.decision import DecisionSchema

router = APIRouter(prefix="/decisions", tags=["Decisions"])

@router.post("/{application_id}")
def decide_application(application_id: int, request: DecisionSchema, db: Session = Depends(get_db)):

    app_data = db.query(Application).filter(Application.id == application_id).first()

    if not app_data:
        return {"detail": "Application not found"}

    if request.decision not in ["approved", "rejected"]:
        return {"detail": "Decision must be approved or rejected"}

    app_data.current_status = request.decision.upper()
    db.commit()

    return {
        "application_id": application_id,
        "new_status": request.decision
    }
