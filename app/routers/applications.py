# app/routers/applications.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)

@router.get("/ping")
def ping_applications():
    return {"resource": "applications", "status": "ok"}

# nanti:
# POST /applications        -> mahasiswa mengajukan beasiswa
# GET  /applications/{id}   -> detail 1 pengajuan
