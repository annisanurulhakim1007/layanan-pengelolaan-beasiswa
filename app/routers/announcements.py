# app/routers/announcements.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/announcements",
    tags=["Announcements"]
)

@router.get("/ping")
def ping_announcements():
    return {"resource": "announcements", "status": "ok"}

# nanti:
# GET  /announcements        -> daftar pengumuman
# GET  /announcements/{id}   -> detail
# POST /announcements        -> admin buat pengumuman baru
