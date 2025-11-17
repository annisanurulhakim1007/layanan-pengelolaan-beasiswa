# app/routers/scholarship_types.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/scholarship-types",
    tags=["Scholarship Types"]
)

@router.get("/ping")
def ping_scholarship_types():
    return {"resource": "scholarship-types", "status": "ok"}

# nanti di sini:
# GET /scholarship-types -> list semua jenis beasiswa
# GET /scholarship-types/{id} -> detail satu jenis beasiswa
