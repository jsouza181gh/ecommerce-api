from infrastructure.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey, Index, UniqueConstraint, CheckConstraint, text
from sqlalchemy.orm import relationship

class ProductReviewImage(Base):
    __tablename__ = "product_review_images"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    review_id = Column("review_id", UUID(as_uuid=True), ForeignKey("product_reviews.id", ondelete="CASCADE"), nullable=False)
    title = Column("title", String(50), nullable=True)
    image_url = Column("image_url", String(500), nullable=False)
    position = Column(Integer, nullable=False, default=0)

    review = relationship(
        "ProductReview",
        back_populates="images"
    )

    __table_args__ = (
        Index("idx_review_images_review_position", "review_id", "position"),
        UniqueConstraint("review_id", "position", name="uq_review_image_position"),
        CheckConstraint("position >= 0", name="check_review_image_position"),
    )