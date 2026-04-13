from infrastructure.database.base import Base

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Text, Integer, ForeignKey, Index, CheckConstraint, DateTime, text, func
from sqlalchemy.orm import relationship

class ProductReview(Base):
    __tablename__ = "product_reviews"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    product_id = Column("product_id", UUID(as_uuid=True), ForeignKey("products.id", ondelete="RESTRICT"), nullable=False)
    title = Column("title", String(50), nullable=True)
    score = Column("score", Integer, nullable=False)
    description = Column("description", Text)
    created_at = Column(DateTime, server_default=func.now())

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