# app/routers/requirements.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.scholarship import ScholarshipRequirement
from ..schemas.requirement import (
    RequirementCreate,
    RequirementUpdate,
    RequirementOut,
)

router = APIRouter(
    prefix="/requirements",
    tags=["Requirements"],
)


@router.get("/ping")
def ping_requirements():
    return {"resource": "requirements", "status": "ok"}


# ==============================
# GET /requirements
# List semua requirement
# ==============================
@router.get("/", response_model=list[RequirementOut])
def list_requirements(db: Session = Depends(get_db)):
    requirements = db.query(ScholarshipRequirement).all()
    return requirements


# ==============================
# GET /requirements/{req_id}
# Detail satu requirement
# ==============================
@router.get("/{req_id}", response_model=RequirementOut)
def get_requirement(req_id: int, db: Session = Depends(get_db)):
    req = (
        db.query(ScholarshipRequirement)
        .filter(ScholarshipRequirement.id == req_id)
        .first()
    )
    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement tidak ditemukan",
        )
    return req


# =============================================
# GET /requirements/by-scholarship/{type_id}
# List requirement berdasarkan jenis beasiswa
# Optional filter per periode
# =============================================
@router.get("/by-scholarship/{scholarship_type_id}", response_model=list[RequirementOut])
def list_requirements_by_scholarship(
    scholarship_type_id: int,
    scholarship_period_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    q = db.query(ScholarshipRequirement).filter(
        ScholarshipRequirement.scholarship_type_id == scholarship_type_id
    )

    if scholarship_period_id is not None:
        q = q.filter(
            ScholarshipRequirement.scholarship_period_id == scholarship_period_id
        )

    return q.all()


# ==============================
# POST /requirements
# Tambah requirement baru
# ==============================
@router.post("/", response_model=RequirementOut, status_code=status.HTTP_201_CREATED)
def create_requirement(
    data: RequirementCreate,
    db: Session = Depends(get_db),
):
    new_req = ScholarshipRequirement(
        scholarship_type_id=data.scholarship_type_id,
        scholarship_period_id=data.scholarship_period_id,
        min_gpa=data.min_gpa,
        min_semester=data.min_semester,
        required_documents=data.required_documents,
        other_conditions=data.other_conditions,
    )

    db.add(new_req)
    db.commit()
    db.refresh(new_req)
    return new_req


# ==============================
# PUT /requirements/{req_id}
# Update requirement
# ==============================
@router.put("/{req_id}", response_model=RequirementOut)
def update_requirement(
    req_id: int,
    data: RequirementUpdate,
    db: Session = Depends(get_db),
):
    req = (
        db.query(ScholarshipRequirement)
        .filter(ScholarshipRequirement.id == req_id)
        .first()
    )

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement tidak ditemukan",
        )

    if data.scholarship_type_id is not None:
        req.scholarship_type_id = data.scholarship_type_id
    if data.scholarship_period_id is not None:
        req.scholarship_period_id = data.scholarship_period_id
    if data.min_gpa is not None:
        req.min_gpa = data.min_gpa
    if data.min_semester is not None:
        req.min_semester = data.min_semester
    if data.required_documents is not None:
        req.required_documents = data.required_documents
    if data.other_conditions is not None:
        req.other_conditions = data.other_conditions

    db.commit()
    db.refresh(req)
    return req


# ==============================
# DELETE /requirements/{req_id}
# Hapus requirement
# ==============================
@router.delete("/{req_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_requirement(
    req_id: int,
    db: Session = Depends(get_db),
):
    req = (
        db.query(ScholarshipRequirement)
        .filter(ScholarshipRequirement.id == req_id)
        .first()
    )

    if not req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requirement tidak ditemukan",
        )

    db.delete(req)
    db.commit()
    return None
