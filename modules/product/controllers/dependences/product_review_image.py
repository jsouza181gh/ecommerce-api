from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends

from infrastructure.database.session import get_database
from ...repositories import ProductReviewImageRepository, ProductReviewRepository
from ...services import ProductReviewImageService
from .product_review import get_product_review_repository

def get_review_image_repository(db: Annotated[AsyncSession, Depends(get_database)]) -> ProductReviewImageRepository:
    return ProductReviewImageRepository(db)


def get_review_image_service(
    review_image_repository: Annotated[ProductReviewImageRepository, Depends(get_review_image_repository)],
    review_repository: Annotated[ProductReviewRepository, Depends(get_product_review_repository)]
):
    return ProductReviewImageService(review_image_repository, review_repository)

ProductReviewImageDependences = Annotated[
    ProductReviewImageService,
    Depends(get_review_image_service)
]