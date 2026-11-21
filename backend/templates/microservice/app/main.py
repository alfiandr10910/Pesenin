from fastapi import FastAPI

from app.db.base import Base
from app.db.session import engine
from app.views.{{entity_snake}} import router as {{entity_snake}}_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="{{service_title}}")
app.include_router({{entity_snake}}_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
