from pydantic import BaseModel, EmailStr, Field


class MahasiswaBase(BaseModel):
    nim: str = Field(min_length=1, max_length=32)
    nama_depan: str = Field(min_length=1, max_length=100)
    nama_belakang: str = Field(min_length=1, max_length=100)
    email: EmailStr


class MahasiswaCreate(MahasiswaBase):
    password: str = Field(min_length=6, max_length=128)


class MahasiswaUpdate(BaseModel):
    nama_depan: str | None = Field(default=None, min_length=1, max_length=100)
    nama_belakang: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=6, max_length=128)


class MahasiswaResponse(MahasiswaBase):
    model_config = {"from_attributes": True}


class CredentialVerifyRequest(BaseModel):
    email: EmailStr
    password: str


class CredentialVerifyResponse(BaseModel):
    nim: str
    email: EmailStr
