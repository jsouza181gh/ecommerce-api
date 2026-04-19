from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from infrastructure.database.session import get_database
from ...repositories import ProductImageRepository, ProductRepository
from ...services import ProductImageService
from .product import get_product_repository

def get_product_image_repository(db: Annotated[AsyncSession, Depends(get_database)]) -> ProductImageRepository:
    return ProductImageRepository(db)

def get_product_image_service(
    product_image_repository: Annotated[ProductImageRepository, Depends(get_product_image_repository)],
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)]

) -> ProductImageService:
    return ProductImageService(product_image_repository, product_repository)

ProductImageDependences = Annotated[
    ProductImageService,
    Depends(get_product_image_service)
]