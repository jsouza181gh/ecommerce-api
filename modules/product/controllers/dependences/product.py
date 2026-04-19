from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from infrastructure.database.session import get_database
from ...repositories import ProductRepository, ProductCategoryRepository
from ...services import ProductService
from .product_category import get_product_category_repository

def get_product_repository(db: Annotated[AsyncSession, Depends(get_database)]) -> ProductRepository:
    return ProductRepository(db)

def get_product_service(
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)],
    category_repository: Annotated[ProductCategoryRepository, Depends(get_product_category_repository)]
) -> ProductService:
    return ProductService(product_repository, category_repository)

ProductDependences = Annotated[
    ProductService,
    Depends(get_product_service)
]