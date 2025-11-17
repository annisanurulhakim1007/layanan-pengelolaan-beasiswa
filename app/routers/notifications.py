# app/routers/notifications.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)

@router.get("/ping")
def ping_notifications():
    return {"resource": "notifications", "status": "ok"}

# nanti:
# GET /notifications/{student_id} -> daftar notifikasi untuk 1 mahasiswa
# atau GET /me/notifications
