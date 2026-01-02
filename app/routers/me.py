# app/routers/me.py
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..models.student import Student
from ..security import get_current_user


router = APIRouter(
    prefix="/me",
    tags=["Student Profile"]
)

@router.get("/ping")
def ping_me():
    return {"resource": "me", "status": "ok"}

# nanti di sini:
# GET /me -> kembalikan profil user yang sedang login


@router.get("/")
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # diasumsikan username == nim
    student = db.query(Student).filter(Student.nim == current_user.username).first()

    if not student:
        return {
            "message": "User ditemukan, tetapi belum memiliki data student",
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "role": current_user.role
            },
            "student_profile": None
        }

    return {
        "user": {
            "id": current_user.id,
            "username": current_user.username,
            "role": current_user.role
        },
        "student_profile": {
            "nim": student.nim,
            "name": student.name,
            "study_program": student.study_program,
            "semester": student.semester,
            "email": student.email,
            "phone": student.phone,
        }
    }