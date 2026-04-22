from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from ..schemas import SaveProductImageSchema, ProductImageSchema
from .dependences import ProductImageDependences

router = APIRouter(prefix='/product_images', tags=['Product Image'])

@router.post(
    '/',
    response_model=ProductImageSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_product_image(
    product_image_service: ProductImageDependences,
    payload: SaveProductImageSchema
):
    new_image = await product_image_service.create(payload)

    return new_image


@router.get(
    '/{image_id}',
    response_model=ProductImageSchema,
    status_code=status.HTTP_200_OK
)
async def get_product_image(
    product_image_service: ProductImageDependences,
    image_id: UUID
):
    image = await product_image_service.find_by_id(image_id)

    return image


@router.get(
    '/',
    response_model=List[ProductImageSchema],
    status_code=status.HTTP_200_OK
)
async def list_product_images(
    product_image_service: ProductImageDependences
):
    images = await product_image_service.find_all()

    return images


@router.put(
    '/{image_id}',
    response_model=ProductImageSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_product_image(
    product_image_service: ProductImageDependences,
    payload: SaveProductImageSchema,
    image_id: UUID
):
    new_image = await product_image_service.update(image_id, payload)

    return new_image


@router.delete(
    '/{image_id}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product_image(
    product_image_service: ProductImageDependences,
    image_id: UUID
):
    await product_image_service(image_id)