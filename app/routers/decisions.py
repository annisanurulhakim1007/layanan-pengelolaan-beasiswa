# app/routers/decisions.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/decisions",
    tags=["Admin Decisions"]
)

@router.get("/ping")
def ping_decisions():
    return {"resource": "decisions", "status": "ok"}

# nanti:
# POST /decisions/{application_id}
# body -> { "decision": "ACCEPTED/REJECTED", "note": "..." }
# akan update status aplikasi + tulis ke status_history + buat notifikasi
