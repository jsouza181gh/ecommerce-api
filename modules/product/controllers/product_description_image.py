from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from ..schemas import SaveProductDescriptionImageSchema, ProductDescriptionImageSchema
from .dependencies import ProductDescriptionImageDependencies

router = APIRouter(prefix='/description-images', tags=['Product Description Image'])

@router.post(
    '/',
    response_model=ProductDescriptionImageSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_description_image(
    payload: SaveProductDescriptionImageSchema,
    description_image_service: ProductDescriptionImageDependencies
):
    new_description_image = await description_image_service.create(payload)

    return new_description_image


@router.get(
    '/{description_image_id}',
    response_model=ProductDescriptionImageSchema,
    status_code=status.HTTP_200_OK
)
async def get_description_image(
    description_image_id: UUID,
    description_image_service: ProductDescriptionImageDependencies
):
    description_image = await description_image_service.find_by_id(description_image_id)

    return description_image


@router.get(
    '/',
    response_model=List[ProductDescriptionImageSchema],
    status_code=status.HTTP_200_OK
)
async def list_description_images(
    description_image_service: ProductDescriptionImageDependencies
):
    description_images = await description_image_service.find_all()

    return description_images


@router.put(
    '/{description_image_id}',
    response_model=ProductDescriptionImageSchema,
    status_code=status.HTTP_200_OK
)
async def update_description_image(
    description_image_id: UUID,
    payload: SaveProductDescriptionImageSchema,
    description_image_service: ProductDescriptionImageDependencies
):
    new_description_image = await description_image_service.update(description_image_id, payload)

    return new_description_image


@router.delete(
    '/{description_image_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_description_image(
    description_image_id: UUID,
    description_image_service: ProductDescriptionImageDependencies
):
    await description_image_service.delete(description_image_id)