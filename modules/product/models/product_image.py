from infrastructure.database.base import Base

from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Integer, ForeignKey, Index, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column ,relationship

class ProductImage(Base):
    __tablename__ = "product_images"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id: Mapped[UUID] = mapped_column("product_id", PG_UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column("title", String(50), nullable=True)
    image_url: Mapped[str] = mapped_column("image_url", String(500), nullable=False, unique=True)
    position: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    product = relationship(
        "Product",
        back_populates="images"
    )

    __table_args__ = (
        Index("idx_product_images_product_position", "product_id", "position"),
        UniqueConstraint("product_id", "position", name="uq_product_image_position"),
        CheckConstraint("position >= 0", name="check_product_image_position"),
    )