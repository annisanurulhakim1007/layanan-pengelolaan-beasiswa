# app/routers/documents.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Application Documents"]
)

@router.get("/ping")
def ping_documents():
    return {"resource": "documents", "status": "ok"}

# nanti:
# POST /applications/{id}/documents -> upload dokumen pendukung
# GET  /applications/{id}/documents -> list dokumen untuk 1 pengajuan
