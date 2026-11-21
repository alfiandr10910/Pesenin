from decimal import Decimal

from pydantic import BaseModel, Field


class PesananItemCreate(BaseModel):
    id_menu: str = Field(min_length=1, max_length=32)
    qty: int = Field(default=1, ge=1)


class PesananItemResponse(BaseModel):
    id_menu: str
    nama_menu: str
    harga_saat_pesan: Decimal
    qty: int
    model_config = {"from_attributes": True}


class PesananCreate(BaseModel):
    id_pesanan: str = Field(min_length=1, max_length=32)
    nomor_pesanan: str = Field(min_length=1, max_length=64)
    id_tenant: str = Field(min_length=1, max_length=32)
    items: list[PesananItemCreate] = Field(min_length=1)


class PesananStatusUpdate(BaseModel):
    status_pesanan: str = Field(min_length=1, max_length=32)


class PesananResponse(BaseModel):
    id_pesanan: str
    nomor_pesanan: str
    total_harga: Decimal
    status_pesanan: str
    nim: str
    id_tenant: str
    items: list[PesananItemResponse]
    model_config = {"from_attributes": True}
