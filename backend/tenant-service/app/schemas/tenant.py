from pydantic import BaseModel, EmailStr, Field


class TenantBase(BaseModel):
    id_tenant: str = Field(min_length=1, max_length=32)
    nama_toko: str = Field(min_length=1, max_length=150)
    email: EmailStr


class TenantCreate(TenantBase):
    password: str = Field(min_length=6, max_length=128)


class TenantUpdate(BaseModel):
    nama_toko: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=128)


class TenantResponse(TenantBase):
    model_config = {"from_attributes": True}


class CredentialVerifyRequest(BaseModel):
    email: EmailStr
    password: str


class CredentialVerifyResponse(BaseModel):
    id_tenant: str
    email: EmailStr
