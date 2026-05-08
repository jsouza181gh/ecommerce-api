from infrastructure.database.base import Base

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, Index, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import relationship

class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    title = Column("title", String(50), nullable=True)
    image_url = Column("image_url", String(500), nullable=False, unique=True)
    position = Column(Integer, nullable=False, default=0)

    product = relationship(
        "Product",
        back_populates="images"
    )

    __table_args__ = (
        Index("idx_product_images_product_position", "product_id", "position"),
        UniqueConstraint("product_id", "position", name="uq_product_image_position"),
        CheckConstraint("position >= 0", name="check_product_image_position"),
    )