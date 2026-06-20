from infrastructure.database.base import Base

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, text, func
from datetime import datetime
from uuid import UUID

class Role(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column("name", String(30), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    users = relationship(
        "User",
        back_populates="role"
    )

    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles"
    )