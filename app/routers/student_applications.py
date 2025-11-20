from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..models.application import Application
from ..schemas.application import ApplicationRead

router = APIRouter(
    prefix="/student-applications",
    tags=["Student Applications"],
)


@router.get("/{student_id}", response_model=List[ApplicationRead])
def get_applications_by_student(student_id: int, db: Session = Depends(get_db)):
    """
    Mengambil semua pengajuan beasiswa milik satu mahasiswa (berdasarkan student_id).
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    apps = db.query(Application).filter(Application.student_id == student_id).all()
    return apps
