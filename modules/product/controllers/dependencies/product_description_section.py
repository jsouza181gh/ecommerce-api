from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from infrastructure.database.session import get_database
from ...repositories import ProductDescriptionSectionRepository, ProductRepository
from ...services import ProductDescriptionSectionService
from .product import get_product_repository

def get_product_description_section_repository(db: Annotated[AsyncSession, Depends(get_database)]):
    return ProductDescriptionSectionRepository(db)


def get_product_description_section_service(
    description_repository: Annotated[ProductDescriptionSectionRepository, Depends(get_product_description_section_repository)],
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)]
):
    return ProductDescriptionSectionService(description_repository, product_repository)

ProductDescriptionSectionDependencies = Annotated[
    ProductDescriptionSectionService,
    Depends(get_product_description_section_service)
]