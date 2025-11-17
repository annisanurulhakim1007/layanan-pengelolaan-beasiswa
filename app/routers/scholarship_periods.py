# app/routers/scholarship_periods.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/scholarship-periods",
    tags=["Scholarship Periods"]
)

@router.get("/ping")
def ping_scholarship_periods():
    return {"resource": "scholarship-periods", "status": "ok"}

# nanti:
# GET /scholarship-periods -> list periode
# GET /scholarship-periods/{id} -> detail
