from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.views.pesanan import router as pesanan_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pesanan Service")
app.include_router(pesanan_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
