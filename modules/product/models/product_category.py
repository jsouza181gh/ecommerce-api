from infrastructure.database.base import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, text
from sqlalchemy.orm import relationship

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column("name", String(50), nullable=False, unique=True)
    
    products = relationship(
        "Product",
        back_populates="category"
    )