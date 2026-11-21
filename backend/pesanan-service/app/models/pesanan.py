from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Pesanan(Base):
    __tablename__ = "pesanan"

    id_pesanan: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    nomor_pesanan: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    total_harga: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    status_pesanan: Mapped[str] = mapped_column(String(32), nullable=False, default="pending")
    nim: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    id_tenant: Mapped[str] = mapped_column(String(32), index=True, nullable=False)

    items = relationship("PesananMenu", back_populates="pesanan", cascade="all, delete-orphan")
