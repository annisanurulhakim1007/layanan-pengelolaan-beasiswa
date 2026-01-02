# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.user import User
from ..security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/ping")
def ping_auth():
    return {"resource": "auth", "status": "ok"}


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # form.username itu bisa email/username. Di sistem kamu = username (admin) atau NIM (mahasiswa)
    user = db.query(User).filter(User.username == form.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username atau password salah"
        )

    if not verify_password(form.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username atau password salah"
        )

    token = create_access_token(sub=str(user.id), role=user.role)
    return {"access_token": token, "token_type": "bearer"}
