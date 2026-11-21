import httpx
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse


class AuthController:
    @staticmethod
    async def _verify_with_service(base_url: str, payload: LoginRequest) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(f"{base_url}/internal/verify-credentials", json=payload.model_dump())
            except httpx.RequestError as exc:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Auth dependency unavailable: {exc}") from exc
        if response.status_code == status.HTTP_401_UNAUTHORIZED:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if response.status_code >= 400:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Credential verification failed")
        return response.json()

    @staticmethod
    async def login_mahasiswa(payload: LoginRequest) -> TokenResponse:
        user = await AuthController._verify_with_service(settings.mahasiswa_service_url, payload)
        token = create_access_token(subject=user["nim"], role="mahasiswa", extra={"nim": user["nim"]})
        return TokenResponse(access_token=token, role="mahasiswa", subject=user["nim"])

    @staticmethod
    async def login_tenant(payload: LoginRequest) -> TokenResponse:
        user = await AuthController._verify_with_service(settings.tenant_service_url, payload)
        token = create_access_token(subject=user["id_tenant"], role="tenant", extra={"id_tenant": user["id_tenant"]})
        return TokenResponse(access_token=token, role="tenant", subject=user["id_tenant"])
