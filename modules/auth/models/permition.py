from infrastructure.database.base import Base

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text
from uuid import UUID

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column("name", String(30), unique=True, nullable=False)

    roles = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions"
    )