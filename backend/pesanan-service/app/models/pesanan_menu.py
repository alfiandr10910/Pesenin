from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class PesananMenu(Base):
    __tablename__ = "pesanan_menu"

    id_pesanan: Mapped[str] = mapped_column(ForeignKey("pesanan.id_pesanan", ondelete="CASCADE"), primary_key=True)
    id_menu: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    nama_menu: Mapped[str] = mapped_column(String(150), nullable=False)
    harga_saat_pesan: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    qty: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    pesanan = relationship("Pesanan", back_populates="items")
