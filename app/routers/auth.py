# app/routers/auth.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.get("/ping")
def ping_auth():
    return {"resource": "auth", "status": "ok"}

# nanti di sini kamu tambahkan:
# POST /auth/login  (login admin/mahasiswa, return JWT)
