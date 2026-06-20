from infrastructure.database.base import Base

from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from uuid import UUID

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column("role_id", PG_UUID(as_uuid=True), ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, primary_key=True)
    permission_id: Mapped[UUID] = mapped_column("permission_id", PG_UUID(as_uuid=True), ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False, primary_key=True)