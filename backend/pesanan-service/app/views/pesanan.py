from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.controllers.pesanan_controller import PesananController
from app.core.security import get_current_claims, require_role
from app.db.session import get_db
from app.schemas.pesanan import PesananCreate, PesananResponse, PesananStatusUpdate

router = APIRouter(prefix="/pesanan", tags=["pesanan"])
bearer_scheme = HTTPBearer(auto_error=False)


@router.post("", response_model=PesananResponse, status_code=status.HTTP_201_CREATED)
async def create_pesanan(
    payload: PesananCreate,
    claims: dict = Depends(require_role("mahasiswa")),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    return await PesananController.create(db, payload, claims["sub"], credentials.credentials)


@router.get("", response_model=list[PesananResponse])
def list_pesanan(claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return PesananController.list(db, claims.get("role"), claims.get("sub"))


@router.get("/{id_pesanan}", response_model=PesananResponse)
def get_pesanan(id_pesanan: str, claims: dict = Depends(get_current_claims), db: Session = Depends(get_db)):
    return PesananController.get(db, id_pesanan, claims.get("role"), claims.get("sub"))


@router.patch("/{id_pesanan}/status", response_model=PesananResponse)
def update_status(
    id_pesanan: str,
    payload: PesananStatusUpdate,
    claims: dict = Depends(require_role("tenant")),
    db: Session = Depends(get_db),
):
    return PesananController.update_status(db, id_pesanan, claims.get("sub"), payload)
