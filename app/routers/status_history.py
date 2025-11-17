# app/routers/status_history.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/status-history",
    tags=["Status History"]
)

@router.get("/ping")
def ping_status_history():
    return {"resource": "status-history", "status": "ok"}

# nanti:
# GET /status-history/{application_id} -> riwayat status 1 pengajuan
