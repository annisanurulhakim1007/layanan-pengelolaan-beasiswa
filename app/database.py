# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Engine: pintu utama koneksi ke PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal: "session" untuk tiap request ke DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base: kelas dasar yang akan diwarisi semua model
Base = declarative_base()

# Dependency: dipakai di router (FastAPI) untuk dapat session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
