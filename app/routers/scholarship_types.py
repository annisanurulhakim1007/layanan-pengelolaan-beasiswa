# app/routers/scholarship_types.py
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.scholarship import ScholarshipType
from ..schemas.scholarship_type import (
    ScholarshipTypeCreate,
    ScholarshipTypeUpdate,
    ScholarshipTypeOut,
)

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




# ==============================
# GET /scholarship-types
# List semua jenis beasiswa
# ==============================
@router.get("/", response_model=list[ScholarshipTypeOut])
def list_scholarship_types(db: Session = Depends(get_db)):
    types = db.query(ScholarshipType).all()
    return types


# ==============================
# GET /scholarship-types/{id}
# Detail satu jenis beasiswa
# ==============================
@router.get("/{type_id}", response_model=ScholarshipTypeOut)
def get_scholarship_type(type_id: int, db: Session = Depends(get_db)):
    stype = db.query(ScholarshipType).filter(ScholarshipType.id == type_id).first()
    if not stype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis beasiswa tidak ditemukan",
        )
    return stype


# ==============================
# POST /scholarship-types
# Tambah jenis beasiswa
# ==============================
# app/routers/scholarship_types.py

@router.post("/", response_model=ScholarshipTypeOut, status_code=status.HTTP_201_CREATED)
def create_scholarship_type(
    data: ScholarshipTypeCreate,
    db: Session = Depends(get_db),
):
    # Cek kode unik
    existing_code = db.query(ScholarshipType).filter(ScholarshipType.code == data.code).first()
    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kode jenis beasiswa sudah digunakan",
        )

    # Cek nama unik (opsional tapi bagus)
    existing_name = db.query(ScholarshipType).filter(ScholarshipType.name == data.name).first()
    if existing_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nama jenis beasiswa sudah digunakan",
        )

    new_type = ScholarshipType(
        code=data.code,
        name=data.name,
        description=data.description,
        is_active=data.is_active,
    )
    db.add(new_type)
    db.commit()
    db.refresh(new_type)
    return new_type


# ==============================
# PUT /scholarship-types/{id}
# Update jenis beasiswa
# ==============================
@router.put("/{type_id}", response_model=ScholarshipTypeOut)
def update_scholarship_type(
    type_id: int,
    data: ScholarshipTypeUpdate,
    db: Session = Depends(get_db),
):
    stype = db.query(ScholarshipType).filter(ScholarshipType.id == type_id).first()
    if not stype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis beasiswa tidak ditemukan",
        )

    if data.name is not None:
        stype.name = data.name
    if data.description is not None:
        stype.description = data.description

    db.commit()
    db.refresh(stype)
    return stype


# ==============================
# DELETE /scholarship-types/{id}
# Hapus jenis beasiswa
# ==============================
@router.delete("/{type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scholarship_type(
    type_id: int,
    db: Session = Depends(get_db),
):
    stype = db.query(ScholarshipType).filter(ScholarshipType.id == type_id).first()
    if not stype:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Jenis beasiswa tidak ditemukan",
        )

    db.delete(stype)
    db.commit()
    return None