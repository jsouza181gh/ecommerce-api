from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from infrastructure.database.session import get_database
from ...repositories import ProductCategoryRepository
from ...services import ProductCategoryService

def get_product_category_repository(db: AsyncSession = Depends(get_database)):
    return ProductCategoryRepository(db)

def get_product_category_service(repository: ProductCategoryRepository = Depends(get_product_category_repository)):
    return ProductCategoryService(repository)

ProductCategoryServiceDependence = Annotated[
    ProductCategoryService,
    Depends(get_product_category_service)
]