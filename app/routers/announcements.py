from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.announcement import AnnouncementCreate, AnnouncementRead
from app.models.announcement import Announcement

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.post("/", response_model=AnnouncementRead)
def create_announcement(data: AnnouncementCreate, db: Session = Depends(get_db)):

    if not data.title or not data.content:
        raise HTTPException(status_code=400, detail="Title and content are required")

    new_announce = Announcement(
        title=data.title,
        content=data.content
    )

    db.add(new_announce)
    db.commit()
    db.refresh(new_announce)

    return new_announce
