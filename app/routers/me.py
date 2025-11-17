# app/routers/me.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/me",
    tags=["Student Profile"]
)

@router.get("/ping")
def ping_me():
    return {"resource": "me", "status": "ok"}

# nanti di sini:
# GET /me -> kembalikan profil user yang sedang login
