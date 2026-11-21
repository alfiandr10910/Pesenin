from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.tenant import Tenant
from app.schemas.tenant import CredentialVerifyRequest, TenantCreate, TenantUpdate


class TenantController:
    @staticmethod
    def create(db: Session, payload: TenantCreate) -> Tenant:
        if db.get(Tenant, payload.id_tenant):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Tenant ID already exists")
        if db.scalar(select(Tenant).where(Tenant.email == payload.email)):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
        tenant = Tenant(
            id_tenant=payload.id_tenant,
            nama_toko=payload.nama_toko,
            email=payload.email,
            password=hash_password(payload.password),
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
        return tenant

    @staticmethod
    def get_by_id(db: Session, id_tenant: str) -> Tenant:
        tenant = db.get(Tenant, id_tenant)
        if not tenant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
        return tenant

    @staticmethod
    def list(db: Session) -> list[Tenant]:
        return list(db.scalars(select(Tenant)).all())

    @staticmethod
    def update(db: Session, id_tenant: str, actor_id: str, payload: TenantUpdate) -> Tenant:
        if actor_id != id_tenant:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update other tenant")
        tenant = TenantController.get_by_id(db, id_tenant)
        if payload.email and payload.email != tenant.email:
            if db.scalar(select(Tenant).where(Tenant.email == payload.email)):
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
            tenant.email = payload.email
        if payload.nama_toko is not None:
            tenant.nama_toko = payload.nama_toko
        if payload.password is not None:
            tenant.password = hash_password(payload.password)
        db.commit()
        db.refresh(tenant)
        return tenant

    @staticmethod
    def verify_credentials(db: Session, payload: CredentialVerifyRequest) -> Tenant:
        tenant = db.scalar(select(Tenant).where(Tenant.email == payload.email))
        if not tenant or not verify_password(payload.password, tenant.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return tenant
