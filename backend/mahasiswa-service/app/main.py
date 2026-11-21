from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.views.mahasiswa import internal_router, router as mahasiswa_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mahasiswa Service")
app.include_router(mahasiswa_router)
app.include_router(internal_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
