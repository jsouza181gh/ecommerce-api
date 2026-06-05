from infrastructure.database.base import Base

from uuid import UUID
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name: Mapped[str] = mapped_column("name", String(50), nullable=False, unique=True)
    
    products = relationship(
        "Product",
        back_populates="category"
    )