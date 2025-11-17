# app/routers/review_queue.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/review-queue",
    tags=["Review Queue (Admin)"]
)

@router.get("/ping")
def ping_review_queue():
    return {"resource": "review-queue", "status": "ok"}

# nanti:
# GET /review-queue?status=PENDING -> list pengajuan yang perlu diverifikasi admin
