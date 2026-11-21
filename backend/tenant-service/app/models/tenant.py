from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenant"

    id_tenant: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    nama_toko: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    menus = relationship("Menu", back_populates="tenant", cascade="all, delete-orphan")
