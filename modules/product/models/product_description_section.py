from infrastructure.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import relationship

class ProductDescriptionSection(Base):
    __tablename__ = "product_description_sections"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    title = Column("title", String(50), nullable=False)
    subtitle = Column("subtitle", String(100), nullable=True)
    description = Column("description", Text, nullable=False)
    position = Column(Integer, nullable=False, default=0)
    
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