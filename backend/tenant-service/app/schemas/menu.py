from decimal import Decimal

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    id_menu: str = Field(min_length=1, max_length=32)
    nama_menu: str = Field(min_length=1, max_length=150)
    harga: Decimal = Field(gt=0)
    stok: int = Field(ge=0)


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    nama_menu: str | None = Field(default=None, min_length=1, max_length=150)
    harga: Decimal | None = Field(default=None, gt=0)
    stok: int | None = Field(default=None, ge=0)


class MenuResponse(MenuBase):
    id_tenant: str
    model_config = {"from_attributes": True}
