from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.{{entity_snake}} import {{entity_pascal}}
from app.schemas.{{entity_snake}} import {{entity_pascal}}Create, {{entity_pascal}}Update


class {{entity_pascal}}Controller:
    @staticmethod
    def create(db: Session, payload: {{entity_pascal}}Create) -> {{entity_pascal}}:
        if db.get({{entity_pascal}}, payload.id):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="ID already exists")
        obj = {{entity_pascal}}(**payload.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def list(db: Session) -> list[{{entity_pascal}}]:
        return list(db.scalars(select({{entity_pascal}})).all())

    @staticmethod
    def get(db: Session, id: str) -> {{entity_pascal}}:
        obj = db.get({{entity_pascal}}, id)
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
        return obj

    @staticmethod
    def update(db: Session, id: str, payload: {{entity_pascal}}Update) -> {{entity_pascal}}:
        obj = {{entity_pascal}}Controller.get(db, id)
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj, field, value)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, id: str) -> None:
        obj = {{entity_pascal}}Controller.get(db, id)
        db.delete(obj)
        db.commit()
