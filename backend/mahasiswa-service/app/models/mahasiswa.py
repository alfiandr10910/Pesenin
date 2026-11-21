from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Mahasiswa(Base):
    __tablename__ = "mahasiswa"

    nim: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    nama_depan: Mapped[str] = mapped_column(String(100), nullable=False)
    nama_belakang: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
