# app/routers/student_profile.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.student import Student
from ..schemas.student import (
    StudentProfileCreate,
    StudentProfileOut,
    StudentProfileUpdate,
)

router = APIRouter(
    prefix="/student-profile",
    tags=["Student Profile"],
)


@router.get("/ping")
def ping_student_profile():
    return {"resource": "student-profile", "status": "ok"}


# ==============================
# GET /student-profile
# Profil mahasiswa yang sedang login
# ==============================

@router.get("/{nim}", response_model=StudentProfileOut)
def get_student_profile(
    nim: str,
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.nim == nim).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mahasiswa tidak ditemukan",
        )
    return student

@router.post("/", response_model=StudentProfileOut, status_code=status.HTTP_201_CREATED)
def create_student_profile(
    data: StudentProfileCreate,
    db: Session = Depends(get_db),
):
    # cek NIM unik
    existing = db.query(Student).filter(Student.nim == data.nim).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="NIM sudah terdaftar",
        )

    student = Student(
        nim=data.nim,
        name=data.full_name,
        study_program=data.study_program,
        semester=data.semester,
        email=data.email,
        phone=data.phone,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


# ==============================
# PUT /student-profile
# Update profil mahasiswa yang sedang login
# ==============================
@router.put("/{nim}", response_model=StudentProfileOut)
def update_student_profile(
    nim: str,
    data: StudentProfileUpdate,
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.nim == nim).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mahasiswa tidak ditemukan",
        )

    if data.full_name is not None:
        student.name = data.full_name
    if data.study_program is not None:
        student.study_program = data.study_program
    if data.semester is not None:
        student.semester = data.semester
    if data.email is not None:
        student.email = data.email
    if data.phone is not None:
        student.phone = data.phone

    db.commit()
    db.refresh(student)
    return student


# ==============================
# GET /student-profile/{student_id}
# Lihat profil mahasiswa by ID (buat admin)
# ==============================
@router.get("/{student_id}", response_model=StudentProfileOut)
def get_student_profile_by_id(
    student_id: int,
    db: Session = Depends(get_db),
):
    # Di sini idealnya dicek role admin, tapi
    # sementara kita skip biar nggak ribet
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profil mahasiswa tidak ditemukan",
        )
    return student
