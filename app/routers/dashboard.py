from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..database import get_db
from ..models.application import Application
from ..models.application import ApplicationStatus
from ..models.application import ApplicationDocument

router = APIRouter(prefix="/dashboard-metrics", tags=["Dashboard Metrics"])

@router.get("/")
def get_dashboard_metrics(db: Session = Depends(get_db)):
    """
    Statistik ringkas untuk admin.
    Tidak pakai schema dulu, karena output agregasi lebih fleksibel.
    """
    total_apps = db.query(func.count(Application.id)).scalar()

    by_status = (
        db.query(Application.current_status, func.count(Application.id))
        .group_by(Application.current_status)
        .all()
    )
    status_map = {str(s): c for s, c in by_status}

    total_docs = db.query(func.count(ApplicationDocument.id)).scalar()

    last_7_days = datetime.utcnow() - timedelta(days=7)
    recent_apps = (
        db.query(func.count(Application.id))
        .filter(Application.created_at >= last_7_days)
        .scalar()
    )

    return {
        "total_applications": total_apps,
        "applications_by_status": status_map,
        "total_documents": total_docs,
        "applications_last_7_days": recent_apps,
    }
