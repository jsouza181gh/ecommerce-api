from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends

from infrastructure.database.session import get_database
from ...repositories import ProductReviewRepository, ProductRepository
from ...services import ProductReviewService
from .product import get_product_repository

def get_product_review_repository(db: Annotated[AsyncSession, Depends(get_database)]):
    return ProductReviewRepository(db)


def get_product_review_service(
    review_repository: Annotated[ProductReviewRepository, Depends(get_product_review_repository)],
    product_repository: Annotated[ProductRepository, Depends(get_product_repository)]
):
    return ProductReviewService(review_repository, product_repository)


ProductReviewDependences = Annotated[
    ProductReviewService,
    Depends(get_product_review_service)
]