# app/routers/requirements.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/requirements",
    tags=["Scholarship Requirements"]
)

@router.get("/ping")
def ping_requirements():
    return {"resource": "requirements", "status": "ok"}

# nanti:
# GET /requirements?type_id=..&period_id=.. -> syarat untuk jenis/periode tertentu
