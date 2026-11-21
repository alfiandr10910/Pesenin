from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.tenant_controller import TenantController
from app.core.security import get_current_claims, require_role
from app.db.session import get_db
from app.schemas.tenant import (
    CredentialVerifyRequest,
    CredentialVerifyResponse,
    TenantCreate,
    TenantResponse,
    TenantUpdate,
)

router = APIRouter(prefix="/tenant", tags=["tenant"])
internal_router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(payload: TenantCreate, db: Session = Depends(get_db)):
    return TenantController.create(db, payload)


@router.get("/me", response_model=TenantResponse)
def get_me(claims: dict = Depends(require_role("tenant")), db: Session = Depends(get_db)):
    return TenantController.get_by_id(db, claims.get("sub"))


@router.get("/{id_tenant}", response_model=TenantResponse)
def get_tenant(id_tenant: str, _: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return TenantController.get_by_id(db, id_tenant)


@router.get("", response_model=list[TenantResponse])
def list_tenant(_: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return TenantController.list(db)


@router.patch("/{id_tenant}", response_model=TenantResponse)
def update_tenant(
    id_tenant: str,
    payload: TenantUpdate,
    claims: dict = Depends(require_role("tenant")),
    db: Session = Depends(get_db),
):
    return TenantController.update(db, id_tenant, claims.get("sub"), payload)


@internal_router.post("/verify-credentials", response_model=CredentialVerifyResponse)
def verify_credentials(payload: CredentialVerifyRequest, db: Session = Depends(get_db)):
    tenant = TenantController.verify_credentials(db, payload)
    return CredentialVerifyResponse(id_tenant=tenant.id_tenant, email=tenant.email)
