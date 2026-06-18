from fastapi import APIRouter, status
from typing import List
from uuid import UUID

from ..schemas.product import SaveProductSchema, ProductSchema
from .dependencies import ProductDependencies

router = APIRouter(prefix='/products', tags=['Product'])

@router.post(
    '/',
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    payload: SaveProductSchema,
    product_service: ProductDependencies
):
    new_product = await product_service.create(payload)

    return new_product


@router.get(
    '/{product_id}',
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK
)
async def get_product(
    product_id: UUID,
    product_service: ProductDependencies
):
    product = await product_service.find_by_id(product_id)

    return product


@router.get(
    '/',
    response_model=List[ProductSchema],
    status_code=status.HTTP_200_OK
)
async def list_products(
    product_service: ProductDependencies
):
    products = await product_service.find_all()

    return products


@router.put(
    '/{product_id}',
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK
)
async def update_product(
    product_id: UUID,
    payload: SaveProductSchema,
    product_service: ProductDependencies
):
    new_product = await product_service.update(product_id, payload)

    return new_product


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product_id: UUID,
    product_service: ProductDependencies
):
    await product_service.delete(product_id)