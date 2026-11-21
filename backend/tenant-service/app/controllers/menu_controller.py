from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.models.tenant import Tenant
from app.schemas.menu import MenuCreate, MenuUpdate


class MenuController:
    @staticmethod
    def create(db: Session, id_tenant: str, actor_id: str, payload: MenuCreate) -> Menu:
        if actor_id != id_tenant:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot create menu for other tenant")
        if not db.get(Tenant, id_tenant):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        if db.get(Menu, payload.id_menu):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Menu ID already exists")
        menu = Menu(id_tenant=id_tenant, **payload.model_dump())
        db.add(menu)
        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def list_by_tenant(db: Session, id_tenant: str) -> list[Menu]:
        return list(db.scalars(select(Menu).where(Menu.id_tenant == id_tenant)).all())

    @staticmethod
    def get(db: Session, id_menu: str) -> Menu:
        menu = db.get(Menu, id_menu)
        if not menu:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu not found")
        return menu

    @staticmethod
    def update(db: Session, id_menu: str, actor_id: str, payload: MenuUpdate) -> Menu:
        menu = MenuController.get(db, id_menu)
        if actor_id != menu.id_tenant:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update other tenant menu")
        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(menu, field, value)
        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def delete(db: Session, id_menu: str, actor_id: str) -> None:
        menu = MenuController.get(db, id_menu)
        if actor_id != menu.id_tenant:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot delete other tenant menu")
        db.delete(menu)
        db.commit()
