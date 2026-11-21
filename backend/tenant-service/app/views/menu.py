from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.menu_controller import MenuController
from app.core.security import get_current_claims, require_role
from app.db.session import get_db
from app.schemas.menu import MenuCreate, MenuResponse, MenuUpdate

router = APIRouter(tags=["menu"])


@router.post("/tenant/{id_tenant}/menu", response_model=MenuResponse, status_code=status.HTTP_201_CREATED)
def create_menu(
    id_tenant: str,
    payload: MenuCreate,
    claims: dict = Depends(require_role("tenant")),
    db: Session = Depends(get_db),
):
    return MenuController.create(db, id_tenant, claims.get("sub"), payload)


@router.get("/tenant/{id_tenant}/menu", response_model=list[MenuResponse])
def list_menu_by_tenant(id_tenant: str, _: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return MenuController.list_by_tenant(db, id_tenant)


@router.get("/menu/{id_menu}", response_model=MenuResponse)
def get_menu(id_menu: str, _: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return MenuController.get(db, id_menu)


@router.patch("/menu/{id_menu}", response_model=MenuResponse)
def update_menu(
    id_menu: str,
    payload: MenuUpdate,
    claims: dict = Depends(require_role("tenant")),
    db: Session = Depends(get_db),
):
    return MenuController.update(db, id_menu, claims.get("sub"), payload)


@router.delete("/menu/{id_menu}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu(id_menu: str, claims: dict = Depends(require_role("tenant")), db: Session = Depends(get_db)):
    MenuController.delete(db, id_menu, claims.get("sub"))
