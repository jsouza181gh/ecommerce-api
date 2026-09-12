from infrastructure.database.base import Base

from sqlalchemy.dialects.postgresql import CITEXT, UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Boolean, DateTime, text, func
from datetime import datetime
from uuid import UUID

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    role_id: Mapped[UUID] = mapped_column("role_id", PG_UUID(as_uuid=True), ForeignKey("roles.id"), nullable=False)
    email: Mapped[str] = mapped_column("email", CITEXT, unique=True, nullable=False)
    password: Mapped[str] = mapped_column("password", String, nullable=False)
    first_name: Mapped[str] = mapped_column("first_name", String(50), nullable=False)
    last_name: Mapped[str] = mapped_column("last_name", String(50), nullable=False)
    is_active: Mapped[bool] = mapped_column("is_active", Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    role = relationship(
        "Role",
        back_populates="users",
    )

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan"
    )