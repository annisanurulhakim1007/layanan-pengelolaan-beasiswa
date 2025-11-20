from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..models.application import Application
from ..schemas.application import ApplicationCreate, ApplicationRead

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post("/", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(payload: ApplicationCreate, db: Session = Depends(get_db)):
    """
    Membuat pengajuan beasiswa baru (Application).
    - Memastikan student_id valid (mahasiswa ada di tabel students).
    - Menyimpan pengajuan dengan status awal PENDING.
    """
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    app_obj = Application(
        student_id=payload.student_id,
        scholarship_type_id=payload.scholarship_type_id,
        scholarship_period_id=payload.scholarship_period_id,
        gpa=payload.gpa,
        semester=payload.semester,
        reason=payload.reason,
    )
    db.add(app_obj)
    db.commit()
    db.refresh(app_obj)
    return app_obj


@router.get("/", response_model=List[ApplicationRead])
def list_applications(
    status_filter: ApplicationRead.__fields__["current_status"].annotation | None = None,
    db: Session = Depends(get_db),
):
    """
    Mengambil daftar semua pengajuan beasiswa.
    - Opsional: filter berdasarkan status (PENDING, VERIFIED, ACCEPTED, REJECTED).
    """
    query = db.query(Application)
    if status_filter:
        query = query.filter(Application.current_status == status_filter)
    apps = query.all()
    return apps


@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """
    Mengambil detail satu pengajuan berdasarkan ID.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_obj
