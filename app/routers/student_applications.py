# app/routers/student_applications.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/student-applications",
    tags=["Student Applications"]
)

@router.get("/ping")
def ping_student_applications():
    return {"resource": "student-applications", "status": "ok"}

# nanti:
# GET /student-applications/{student_id}  -> semua pengajuan milik 1 mahasiswa
# atau GET /me/applications (bisa di router 'me')
