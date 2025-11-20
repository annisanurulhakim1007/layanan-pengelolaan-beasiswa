from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import Application, ApplicationDocument
from ..schemas.application import (
    ApplicationDocumentCreate,
    ApplicationDocumentRead,
)

router = APIRouter(
    prefix="/documents",
    tags=["Application Documents"],
)


@router.post(
    "/applications/{application_id}",
    response_model=ApplicationDocumentRead,
    status_code=status.HTTP_201_CREATED,
)
def add_document_to_application(
    application_id: int,
    payload: ApplicationDocumentCreate,
    db: Session = Depends(get_db),
):
    """
    Menambahkan dokumen pendukung ke suatu pengajuan beasiswa.
    - Hanya menyimpan metadata (jenis dokumen, nama file, file_path).
    - Tidak melakukan upload file beneran (sesuai scope tugas).
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    doc = ApplicationDocument(
        application_id=application_id,
        document_type=payload.document_type,
        file_name=payload.file_name,
        file_path=payload.file_path,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@router.get(
    "/applications/{application_id}",
    response_model=List[ApplicationDocumentRead],
)
def list_documents_for_application(application_id: int, db: Session = Depends(get_db)):
    """
    Mengambil semua dokumen pendukung untuk satu pengajuan.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=404, detail="Application not found")

    docs = (
        db.query(ApplicationDocument)
        .filter(ApplicationDocument.application_id == application_id)
        .all()
    )
    return docs
