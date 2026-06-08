from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from .dependences import ProductReviewDependences
from ..schemas import SaveProductReviewSchema, ProductReviewSchema

router = APIRouter(prefix='/product-reviews', tags=['Product Reviews'])

@router.post(
    '/',
    response_model=ProductReviewSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_product_review(
    review_service: ProductReviewDependences,
    payload: SaveProductReviewSchema
):
    new_review = await review_service.create(payload)

    return new_review


@router.get(
    '/{review_id}',
    response_model=ProductReviewSchema,
    status_code=status.HTTP_200_OK
)
async def get_product_review(
    review_service: ProductReviewDependences,
    review_id: UUID
):
    review = await review_service.find_by_id(review_id)

    return review


@router.get(
    '/',
    response_model=List[ProductReviewSchema],
    status_code=status.HTTP_200_OK
)
async def list_product_reviews(
    review_service: ProductReviewDependences,
):
    reviews = await review_service.find_all()
    
    return reviews


@router.put(
    '/{review_id}',
    response_model=ProductReviewSchema,
    status_code=status.HTTP_200_OK
)
async def update_product_review(
    review_service: ProductReviewDependences,
    payload: SaveProductReviewSchema,
    review_id: UUID
):
    new_review = await review_service.update(review_id, payload)

    return new_review


@router.delete(
    '/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_review(
    review_service: ProductReviewDependences,
    review_id: UUID
):
    await review_service.delete(review_id)