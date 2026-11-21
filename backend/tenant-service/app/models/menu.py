from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Menu(Base):
    __tablename__ = "menu"

    id_menu: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    id_tenant: Mapped[str] = mapped_column(ForeignKey("tenant.id_tenant", ondelete="CASCADE"), index=True, nullable=False)
    nama_menu: Mapped[str] = mapped_column(String(150), nullable=False)
    harga: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    stok: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    tenant = relationship("Tenant", back_populates="menus")
