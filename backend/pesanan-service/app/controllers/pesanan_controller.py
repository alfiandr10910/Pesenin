from decimal import Decimal

import httpx
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.pesanan import Pesanan
from app.models.pesanan_menu import PesananMenu
from app.schemas.pesanan import PesananCreate, PesananStatusUpdate


class PesananController:
    @staticmethod
    async def _fetch_menu(id_menu: str, token: str) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.get(
                    f"{settings.tenant_service_url}/menu/{id_menu}",
                    headers={"Authorization": f"Bearer {token}"},
                )
            except httpx.RequestError as exc:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Tenant service unavailable: {exc}") from exc
        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu {id_menu} not found")
        if response.status_code >= 400:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Failed to validate menu")
        return response.json()

    @staticmethod
    async def create(db: Session, payload: PesananCreate, nim: str, token: str) -> Pesanan:
        if db.get(Pesanan, payload.id_pesanan):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Pesanan ID already exists")
        if db.scalar(select(Pesanan).where(Pesanan.nomor_pesanan == payload.nomor_pesanan)):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nomor pesanan already exists")

        total = Decimal("0")
        items: list[PesananMenu] = []
        for item in payload.items:
            menu = await PesananController._fetch_menu(item.id_menu, token)
            if menu["id_tenant"] != payload.id_tenant:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Menu {item.id_menu} does not belong to tenant")
            if menu["stok"] < item.qty:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insufficient stock for menu {item.id_menu}")
            harga = Decimal(str(menu["harga"]))
            total += harga * item.qty
            items.append(PesananMenu(
                id_pesanan=payload.id_pesanan, id_menu=item.id_menu, nama_menu=menu["nama_menu"],
                harga_saat_pesan=harga, qty=item.qty,
            ))

        pesanan = Pesanan(
            id_pesanan=payload.id_pesanan, nomor_pesanan=payload.nomor_pesanan, total_harga=total,
            status_pesanan="pending", nim=nim, id_tenant=payload.id_tenant, items=items,
        )
        db.add(pesanan)
        db.commit()
        db.refresh(pesanan)
        return pesanan

    @staticmethod
    def list(db: Session, role: str, subject: str) -> list[Pesanan]:
        stmt = select(Pesanan)
        if role == "mahasiswa":
            stmt = stmt.where(Pesanan.nim == subject)
        elif role == "tenant":
            stmt = stmt.where(Pesanan.id_tenant == subject)
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return list(db.scalars(stmt).all())

    @staticmethod
    def get(db: Session, id_pesanan: str, role: str, subject: str) -> Pesanan:
        pesanan = db.get(Pesanan, id_pesanan)
        if not pesanan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pesanan not found")
        if role == "mahasiswa" and pesanan.nim != subject:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        if role == "tenant" and pesanan.id_tenant != subject:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
        return pesanan

    @staticmethod
    def update_status(db: Session, id_pesanan: str, actor_id: str, payload: PesananStatusUpdate) -> Pesanan:
        pesanan = db.get(Pesanan, id_pesanan)
        if not pesanan:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pesanan not found")
        if pesanan.id_tenant != actor_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update other tenant pesanan")
        pesanan.status_pesanan = payload.status_pesanan
        db.commit()
        db.refresh(pesanan)
        return pesanan
