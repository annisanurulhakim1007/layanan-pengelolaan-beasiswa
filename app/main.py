# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .models import *  # supaya semua model terdaftar di Base
from .routers import (
    auth_router,
    me_router,
    scholarship_types_router,
    scholarship_periods_router,
    requirements_router,
    applications_router,
    student_applications_router,
    documents_router,
    application_status_router,
    status_history_router,
    review_queue_router,
    decisions_router,
    announcements_router,
    notifications_router,
    dashboard_router,
)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    title="API Layanan Pengelolaan Beasiswa Internal Kampus",
    version="1.0.0",
    description="""
        API untuk pengelolaan:
        - Pengajuan beasiswa (applications)
        - Pengajuan milik mahasiswa (student-applications)
        - Dokumen pendukung (documents)
        - Status pengajuan (application-status)
        - Riwayat perubahan status (status-history)

        Dokumentasi otomatis menggunakan OpenAPI + Swagger UI.
        """,
    contact={
        "name": "Annisa Nurul Hakim",
        "email": "2211521007@student.unand.ac.id",
    },
)


@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "message": "Beasiswa Internal API is running",
        "docs": "/docs",
        "redoc": "/redoc",
        "resources": [
            "/auth",
            "/me",
            "/scholarship-types",
            "/scholarship-periods",
            "/requirements",
            "/applications",
            "/student-applications",
            "/documents",
            "/application-status",
            "/status-history",
            "/review-queue",
            "/decisions",
            "/announcements",
            "/notifications",
            "/dashboard-metrics",
        ],
    }


# Registrasi semua router (15 resource)
app.include_router(auth_router)
app.include_router(me_router)
app.include_router(scholarship_types_router)
app.include_router(scholarship_periods_router)
app.include_router(requirements_router)
app.include_router(applications_router)
app.include_router(student_applications_router)
app.include_router(documents_router)
app.include_router(application_status_router)
app.include_router(status_history_router)
app.include_router(review_queue_router)
app.include_router(decisions_router)
app.include_router(announcements_router)
app.include_router(notifications_router)
app.include_router(dashboard_router)
