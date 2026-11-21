from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.views.menu import router as menu_router
from app.views.tenant import internal_router, router as tenant_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tenant Service")
app.include_router(tenant_router)
app.include_router(internal_router)
app.include_router(menu_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
