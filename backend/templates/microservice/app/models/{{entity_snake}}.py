from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class {{entity_pascal}}(Base):
    __tablename__ = "{{entity_table}}"

    id: Mapped[str] = mapped_column(String(32), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
