# app/routers/scholarship_types.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.scholarship import ScholarshipType
from ..schemas.scholarship import ScholarshipTypeResponse
from typing import List

router = APIRouter(prefix="/scholarship-types", tags=["Scholarship Types"])


@router.get("/", response_model=List[ScholarshipTypeResponse])
def get_scholarship_types(db: Session = Depends(get_db)):
    types = db.query(ScholarshipType).all()
    return types
