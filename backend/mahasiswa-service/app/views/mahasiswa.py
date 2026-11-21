from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.mahasiswa_controller import MahasiswaController
from app.core.security import get_current_claims, require_role
from app.db.session import get_db
from app.schemas.mahasiswa import (
    CredentialVerifyRequest,
    CredentialVerifyResponse,
    MahasiswaCreate,
    MahasiswaResponse,
    MahasiswaUpdate,
)

router = APIRouter(prefix="/mahasiswa", tags=["mahasiswa"])
internal_router = APIRouter(prefix="/internal", tags=["internal"])


@router.post("", response_model=MahasiswaResponse, status_code=status.HTTP_201_CREATED)
def create_mahasiswa(payload: MahasiswaCreate, db: Session = Depends(get_db)):
    return MahasiswaController.create(db, payload)


@router.get("/me", response_model=MahasiswaResponse)
def get_me(claims: dict = Depends(require_role("mahasiswa")), db: Session = Depends(get_db)):
    return MahasiswaController.get_by_nim(db, claims.get("sub"))


@router.get("/{nim}", response_model=MahasiswaResponse)
def get_mahasiswa(nim: str, _: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return MahasiswaController.get_by_nim(db, nim)


@router.get("", response_model=list[MahasiswaResponse])
def list_mahasiswa(_: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return MahasiswaController.list(db)


@router.patch("/{nim}", response_model=MahasiswaResponse)
def update_mahasiswa(
    nim: str,
    payload: MahasiswaUpdate,
    claims: dict = Depends(require_role("mahasiswa")),
    db: Session = Depends(get_db),
):
    return MahasiswaController.update(db, nim, claims.get("sub"), payload)


@internal_router.post("/verify-credentials", response_model=CredentialVerifyResponse)
def verify_credentials(payload: CredentialVerifyRequest, db: Session = Depends(get_db)):
    mahasiswa = MahasiswaController.verify_credentials(db, payload)
    return CredentialVerifyResponse(nim=mahasiswa.nim, email=mahasiswa.email)
