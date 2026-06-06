from config import DEFAULT_CURRENCY
from infrastructure.database.base import Base

from uuid import UUID
from decimal import Decimal
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Numeric, ForeignKey, Index, CheckConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Product(Base):
    __tablename__ = "products"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    category_id: Mapped[UUID] = mapped_column("category_id", PG_UUID(as_uuid=True), ForeignKey("product_categories.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column("title", String(50), nullable=False, unique=True)
    cost: Mapped[Decimal] = mapped_column("cost", Numeric(10,2), nullable=False)
    shipping_cost: Mapped[Decimal] = mapped_column("shipping_cost", Numeric(10,2), nullable=False, default=0)
    currency_code: Mapped[str] = mapped_column("currency_code", String(3), nullable=False, default=DEFAULT_CURRENCY)
    margin_percentage: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False)
    main_image_url: Mapped[str] = mapped_column("main_image_url", String(500), nullable=False)

    category = relationship(
        "ProductCategory",
        back_populates="products"
    )
        
    images = relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    
    description_sections = relationship(
        "ProductDescriptionSection",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    reviews = relationship(
        "ProductReview",
        back_populates="product",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
    Index("idx_products_category_id", "category_id"),
    CheckConstraint("margin_percentage >= 0 AND margin_percentage <= 100", name="check_margin_range"),
    )