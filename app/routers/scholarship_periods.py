# app/routers/scholarship_periods.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.scholarship import ScholarshipPeriod
from ..schemas.scholarship_period import (
    ScholarshipPeriodCreate,
    ScholarshipPeriodUpdate,
    ScholarshipPeriodOut,
)

router = APIRouter(
    prefix="/scholarship-periods",
    tags=["Scholarship Periods"]
)


@router.get("/ping")
def ping_scholarship_periods():
    return {"resource": "scholarship-periods", "status": "ok"}


# ==============================
# GET /scholarship-periods
# List semua periode beasiswa
# ==============================
@router.get("/", response_model=list[ScholarshipPeriodOut])
def list_periods(db: Session = Depends(get_db)):
    periods = db.query(ScholarshipPeriod).all()
    return periods


# ==============================
# GET /scholarship-periods/{id}
# Detail satu periode
# ==============================
@router.get("/{period_id}", response_model=ScholarshipPeriodOut)
def get_period(period_id: int, db: Session = Depends(get_db)):
    period = db.query(ScholarshipPeriod).filter(ScholarshipPeriod.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periode beasiswa tidak ditemukan",
        )
    return period


# ==============================
# POST /scholarship-periods
# Tambah periode beasiswa
# ==============================
@router.post("/", response_model=ScholarshipPeriodOut, status_code=status.HTTP_201_CREATED)
def create_period(
    data: ScholarshipPeriodCreate,
    db: Session = Depends(get_db),
):
    # Optional: pastikan kombinasi year + term_name unik
    existing = (
        db.query(ScholarshipPeriod)
        .filter(
            ScholarshipPeriod.year == data.year,
            ScholarshipPeriod.term_name == data.term_name,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Periode dengan tahun & nama gelombang ini sudah ada",
        )

    period = ScholarshipPeriod(
        year=data.year,
        term_name=data.term_name,
        start_date=data.start_date,
        end_date=data.end_date,
        is_active=data.is_active,
    )
    db.add(period)
    db.commit()
    db.refresh(period)
    return period


# ==============================
# PUT /scholarship-periods/{id}
# Update periode beasiswa
# ==============================
@router.put("/{period_id}", response_model=ScholarshipPeriodOut)
def update_period(
    period_id: int,
    data: ScholarshipPeriodUpdate,
    db: Session = Depends(get_db),
):
    period = db.query(ScholarshipPeriod).filter(ScholarshipPeriod.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periode beasiswa tidak ditemukan",
        )

    if data.year is not None:
        period.year = data.year
    if data.term_name is not None:
        period.term_name = data.term_name
    if data.start_date is not None:
        period.start_date = data.start_date
    if data.end_date is not None:
        period.end_date = data.end_date
    if data.is_active is not None:
        period.is_active = data.is_active

    db.commit()
    db.refresh(period)
    return period


# ==============================
# DELETE /scholarship-periods/{id}
# Hapus periode beasiswa
# ==============================
@router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(
    period_id: int,
    db: Session = Depends(get_db),
):
    period = db.query(ScholarshipPeriod).filter(ScholarshipPeriod.id == period_id).first()
    if not period:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Periode beasiswa tidak ditemukan",
        )

    db.delete(period)
    db.commit()
    return None
