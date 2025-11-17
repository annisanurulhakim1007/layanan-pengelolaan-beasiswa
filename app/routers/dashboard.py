# app/routers/dashboard.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard-metrics",
    tags=["Dashboard Metrics (Admin)"]
)

@router.get("/ping")
def ping_dashboard():
    return {"resource": "dashboard-metrics", "status": "ok"}

# nanti:
# GET /dashboard-metrics -> ringkasan statistik (total pengajuan, total lolos, dll.)
