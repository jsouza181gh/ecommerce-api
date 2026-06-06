from infrastructure.database.base import Base

from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Text, Integer, ForeignKey, Index, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductDescriptionSection(Base):
    __tablename__ = "product_description_sections"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id: Mapped[UUID] = mapped_column("product_id", PG_UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column("title", String(50), nullable=False)
    subtitle: Mapped[str] = mapped_column("subtitle", String(100), nullable=True)
    description: Mapped[str] = mapped_column("description", Text, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    product = relationship(
        "Product",
        back_populates="description_sections"
    )

    images = relationship(
        "ProductDescriptionImage",
        back_populates="description_section",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_product_desc_product_id", "product_id", "position"),
        UniqueConstraint("product_id", "position", name="uq_product_desc_position"),
        CheckConstraint("position >= 0", name="check_desc_position_positive"),
    )