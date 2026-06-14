from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends

from infrastructure.database.session import get_database
from ...repositories import ProductDescriptionImageRepository, ProductDescriptionSectionRepository
from ...services import ProductDescriptionImageService
from .product_description_section import get_product_description_section_repository


def get_decription_image_repository(db: Annotated[AsyncSession, Depends(get_database)]):
    return ProductDescriptionImageRepository(db)


def get_description_image_service(
    description_image_repository: Annotated[ProductDescriptionImageRepository, Depends(get_decription_image_repository)],
    description_section_repository: Annotated[ProductDescriptionSectionRepository, Depends(get_product_description_section_repository)]
):
    return ProductDescriptionImageService(description_image_repository, description_section_repository)

ProductDescriptionImageDependencies = Annotated[
    ProductDescriptionImageService,
    Depends(get_description_image_service)
]