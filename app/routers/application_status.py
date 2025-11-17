# app/routers/application_status.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/application-status",
    tags=["Application Status"]
)

@router.get("/ping")
def ping_application_status():
    return {"resource": "application-status", "status": "ok"}

# nanti:
# GET /application-status/{application_id} -> status terkini 1 pengajuan
