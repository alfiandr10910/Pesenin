from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.{{entity_snake}}_controller import {{entity_pascal}}Controller
from app.db.session import get_db
from app.schemas.{{entity_snake}} import {{entity_pascal}}Create, {{entity_pascal}}Response, {{entity_pascal}}Update

router = APIRouter(prefix="/{{entity_snake}}", tags=["{{entity_snake}}"])


@router.post("", response_model={{entity_pascal}}Response, status_code=status.HTTP_201_CREATED)
def create(payload: {{entity_pascal}}Create, db: Session = Depends(get_db)):
    return {{entity_pascal}}Controller.create(db, payload)


@router.get("", response_model=list[{{entity_pascal}}Response])
def list_all(db: Session = Depends(get_db)):
    return {{entity_pascal}}Controller.list(db)


@router.get("/{id}", response_model={{entity_pascal}}Response)
def get(id: str, db: Session = Depends(get_db)):
    return {{entity_pascal}}Controller.get(db, id)


@router.patch("/{id}", response_model={{entity_pascal}}Response)
def update(id: str, payload: {{entity_pascal}}Update, db: Session = Depends(get_db)):
    return {{entity_pascal}}Controller.update(db, id, payload)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str, db: Session = Depends(get_db)):
    {{entity_pascal}}Controller.delete(db, id)
