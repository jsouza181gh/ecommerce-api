from infrastructure.database.base import Base

from uuid import UUID
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import String, Text, Integer, ForeignKey, Index, CheckConstraint, DateTime, text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

class ProductReview(Base):
    __tablename__ = "product_reviews"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id: Mapped[UUID] = mapped_column("product_id", PG_UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    title: Mapped[str] = mapped_column("title", String(50), nullable=True)
    score: Mapped[int] = mapped_column("score", Integer, nullable=False)
    description: Mapped[str] = mapped_column("description", Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    product = relationship(
        "Product",
        back_populates="reviews"
    )

    images = relationship(
        "ProductReviewImage",
        back_populates="review",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_reviews_product_score", "product_id", "score"),
        CheckConstraint("score >= 1 AND score <= 10", name="check_score_range"),
    )