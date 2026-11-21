from fastapi import APIRouter

from app.controllers.auth_controller import AuthController
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/mahasiswa", response_model=TokenResponse)
async def login_mahasiswa(payload: LoginRequest) -> TokenResponse:
    return await AuthController.login_mahasiswa(payload)


@router.post("/login/tenant", response_model=TokenResponse)
async def login_tenant(payload: LoginRequest) -> TokenResponse:
    return await AuthController.login_tenant(payload)
