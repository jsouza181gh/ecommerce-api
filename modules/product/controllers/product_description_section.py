from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from ..schemas import SaveProductDescriptionSectionSchema, ProductDescriptionSectionSchema
from .dependences import ProductDescriptionSectionDependences

router = APIRouter(prefix='/product_description', tags=['Product Description'])

@router.post(
    '/',
    response_model=ProductDescriptionSectionSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_description_section(
    description_service: ProductDescriptionSectionDependences,
    payload: SaveProductDescriptionSectionSchema
):
    new_description_section = await description_service.create(payload)

    return new_description_section


@router.get(
    '/{section_id}',
    response_model=ProductDescriptionSectionSchema,
    status_code=status.HTTP_200_OK
)
async def get_description_section(
    description_service: ProductDescriptionSectionDependences,
    section_id: UUID
):
    description_section = await description_service.find_by_id(section_id)

    return description_section


@router.get(
    '/',
    response_model=List[ProductDescriptionSectionSchema],
    status_code=status.HTTP_200_OK
)
async def list_description_section(
    description_service: ProductDescriptionSectionDependences
):
    description_sections = await description_service.find_all()
    
    return description_sections


@router.put(
    '/{section_id}',
    response_model=ProductDescriptionSectionSchema,
    status_code=status.HTTP_201_CREATED
)
async def update_description_section(
    description_service: ProductDescriptionSectionDependences,
    payload: SaveProductDescriptionSectionSchema,
    section_id: UUID
):
    new_description_section = await description_service.update(section_id, payload)

    return new_description_section


@router.delete(
    '/{section_id}',
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_description_section(
    description_service: ProductDescriptionSectionDependences,
    section_id: UUID
):
    await description_service.delete(section_id)