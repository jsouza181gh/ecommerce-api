from infrastructure.database.base import Base

from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Integer, ForeignKey, Index, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductDescriptionImage(Base):
    __tablename__ = "product_description_images"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    description_section_id: Mapped[UUID] = mapped_column("description_section_id", PG_UUID(as_uuid=True), ForeignKey("product_description_sections.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column("title", String(50), nullable=True)
    image_url: Mapped[str] = mapped_column("image_url", String(500), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    description_section = relationship(
        "ProductDescriptionSection",
        back_populates="images"
    )

    __table_args__ = (
        Index("idx_description_images_description_position", "description_section_id", "position"),
        UniqueConstraint("description_section_id", "position", name="uq_description_image_position"),
        CheckConstraint("position >= 0", name="check_description_image_position"),
    ) 