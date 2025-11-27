# app/routers/documents.py
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
    summary="Tambahkan dokumen ke pengajuan beasiswa",
    description=(
        "Menambahkan satu dokumen pendukung ke suatu pengajuan beasiswa tertentu.\n\n"
        "Catatan:\n"
        "- Endpoint ini **hanya menyimpan metadata dokumen** (jenis dokumen, nama file, `file_path`).\n"
        "- Tidak melakukan upload file secara fisik (sesuai scope tugas, file dianggap sudah tersimpan di storage)."
    ),
    responses={
        201: {"description": "Dokumen berhasil ditambahkan ke pengajuan."},
        404: {"description": "Pengajuan dengan ID tersebut tidak ditemukan."},
    },
)
def add_document_to_application(
    application_id: int,
    payload: ApplicationDocumentCreate,
    db: Session = Depends(get_db),
):
    """
    Langkah kerja endpoint ini:
    1. Cek apakah pengajuan dengan `application_id` ada di tabel `applications`.
    2. Jika tidak ada → kembalikan HTTP 404 `Application not found`.
    3. Jika ada → buat baris baru di tabel `application_documents` berisi metadata dokumen.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

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
    summary="List dokumen untuk satu pengajuan",
    description=(
        "Mengambil seluruh dokumen pendukung yang terkait dengan satu pengajuan beasiswa.\n\n"
        "Endpoint ini akan:\n"
        "- Memastikan pengajuan dengan `application_id` ada di sistem.\n"
        "- Mengembalikan list dokumen (bisa kosong jika belum ada dokumen yang ditambahkan)."
    ),
    responses={
        200: {"description": "Daftar dokumen berhasil diambil."},
        404: {"description": "Pengajuan dengan ID tersebut tidak ditemukan."},
    },
)
def list_documents_for_application(
    application_id: int,
    db: Session = Depends(get_db),
):
    """
    Endpoint ini berguna untuk:
    - Admin yang ingin mengecek kelengkapan dokumen pengajuan.
    - Sistem lain (misalnya modul verifikasi) yang butuh melihat dokumen apa saja yang sudah diunggah.
    """
    app_obj = db.query(Application).filter(Application.id == application_id).first()
    if not app_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    docs = (
        db.query(ApplicationDocument)
        .filter(ApplicationDocument.application_id == application_id)
        .all()
    )
    return docs
