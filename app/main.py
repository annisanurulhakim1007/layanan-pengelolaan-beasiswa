# app/main.py
from fastapi import FastAPI
from .database import Base, engine
from .models import user  # supaya model terbaca Base
# nanti tambahkan import model lain

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Layanan Pengelolaan Beasiswa Internal Kampus",
    version="1.0.0",
    description="Layanan API berbasis FastAPI untuk pengelolaan beasiswa internal."
)


@app.get("/", tags=["Health Check"])
def read_root():
    return {"message": "Beasiswa API is running"}
