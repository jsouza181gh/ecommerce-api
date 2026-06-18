from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from ..schemas import SaveProductReviewImageSchema, ProductReviewImageSchema
from .dependencies import ProductReviewImageDependencies

router = APIRouter(prefix='/review-images', tags=['Product Review Image'])

@router.post(
    '/',
    response_model=ProductReviewImageSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_review_image(
    payload: SaveProductReviewImageSchema,
    review_image_service: ProductReviewImageDependencies
):
    new_review_image = await review_image_service.create(payload)

    return new_review_image


@router.get(
    '/{review_image_id}',
    response_model=ProductReviewImageSchema,
    status_code=status.HTTP_200_OK
)
async def get_review_image(
    review_image_id: UUID,
    review_image_service: ProductReviewImageDependencies
):
    review_image = await review_image_service.find_by_id(review_image_id)

    return review_image


@router.get(
    '/',
    response_model=List[ProductReviewImageSchema],
    status_code=status.HTTP_200_OK
)
async def list_review_images(
    review_image_service: ProductReviewImageDependencies
):
    review_images = await review_image_service.find_all()

    return review_images


@router.put(
    '/{review_image_id}',
    response_model=ProductReviewImageSchema,
    status_code=status.HTTP_200_OK
)
async def update_review_image(
    review_image_id: UUID,
    new_review_image: SaveProductReviewImageSchema,
    review_image_service: ProductReviewImageDependencies
):
    review_image = await review_image_service.update(review_image_id, new_review_image)

    return review_image


@router.delete(
    '/{review_image_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_review_image(
    review_image_id: UUID,
    review_image_service: ProductReviewImageDependencies
):
    await review_image_service.delete(review_image_id)