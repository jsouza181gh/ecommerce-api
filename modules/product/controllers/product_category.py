from fastapi import APIRouter, Query, status
from typing import Optional, List
from uuid import UUID

from ..schemas import SaveProductCategorySchema, ProductCategorySchema
from .dependences import ProductCategoryDependences
    
router = APIRouter(prefix='/categories', tags=['Product Category'])

@router.post(
    '/',
    response_model=ProductCategorySchema,
    status_code=status.HTTP_201_CREATED
)
async def create_category(
    category_service: ProductCategoryDependences,
    payload: SaveProductCategorySchema
):
    new_category = await category_service.create(payload)

    return new_category


@router.get(
    '/{category_id}',
    response_model=ProductCategorySchema,
    status_code=status.HTTP_200_OK
)
async def get_category(
    category_service: ProductCategoryDependences,
    category_id: UUID
):
    category = await category_service.find_by_id(category_id)

    return category


@router.get(
    '/',
    response_model=List[ProductCategorySchema],
    status_code=status.HTTP_200_OK
)
async def list_categories(
    category_service: ProductCategoryDependences,
    name: Optional[str] = Query(None, min_length=3)
):
    categories = await category_service.find_all(name)

    return categories


@router.put(
    '/{category_id}',
    response_model=ProductCategorySchema,
    status_code=status.HTTP_200_OK
)
async def update_category(
    category_service: ProductCategoryDependences,
    payload: SaveProductCategorySchema,
    category_id: UUID
):
    new_category = await category_service.update(category_id, payload)

    return new_category


@router.delete(
    '/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_category(
    category_service: ProductCategoryDependences,
    category_id: UUID
):
    await category_service.delete(category_id)