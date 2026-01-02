from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..database import get_db
from ..models.announcement import Announcement
from ..schemas.announcement import AnnouncementCreate, AnnouncementRead

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.post("/", response_model=AnnouncementRead, status_code=status.HTTP_201_CREATED)
def create_announcement(payload: AnnouncementCreate, db: Session = Depends(get_db)):
    ann = Announcement(
        title=payload.title,
        content=payload.content,
        scholarship_type_id=payload.scholarship_type_id,
        scholarship_period_id=payload.scholarship_period_id,
        is_published=payload.is_published,
        published_at=datetime.utcnow() if payload.is_published else None
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann

@router.get("/", response_model=List[AnnouncementRead])
def list_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).all()

@router.get("/{announcement_id}", response_model=AnnouncementRead)
def get_announcement(announcement_id: int, db: Session = Depends(get_db)):
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return ann

@router.patch("/{announcement_id}", response_model=AnnouncementRead)
def publish_or_update_announcement(
    announcement_id: int,
    payload: AnnouncementCreate,
    db: Session = Depends(get_db)
):
    """
    Patch sederhana: pakai AnnouncementCreate lagi (biar gak bikin schema baru).
    Efeknya: update title/content dan status publish.
    """
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found")

    ann.title = payload.title
    ann.content = payload.content
    ann.scholarship_type_id = payload.scholarship_type_id
    ann.scholarship_period_id = payload.scholarship_period_id
    ann.is_published = payload.is_published
    ann.published_at = datetime.utcnow() if payload.is_published else None
    ann.updated_at = datetime.utcnow()

    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann
