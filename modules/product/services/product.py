from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID

from ..schemas import SaveProductSchema, ProductSchema
from ..repositories import ProductRepository, ProductCategoryRepository
from ..models import Product

@dataclass
class ProductService:
    product_repository: ProductRepository
    category_repository: ProductCategoryRepository

    async def create(self, product_schema: SaveProductSchema) -> ProductSchema:
        product_category_exists = await self.category_repository.exists(product_schema.category_id)

        if not product_category_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category was not found'
            )

        new_product = self.convert_schema_to_model(product_schema)

        try:
            await self.product_repository.create(new_product)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not create product due to data conflict'
            )

        return ProductSchema.model_validate(new_product)
    

    async def find_by_id(self, product_id: UUID) -> ProductSchema:
        product = await self.product_repository.find_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )

        return ProductSchema.model_validate(product)
    

    async def find_all(self) -> List[ProductSchema]:
        products = await self.product_repository.find_all()

        return [
            ProductSchema.model_validate(product)
            for product in products
        ]
    

    async def update(
        self, 
        product_id: UUID, 
        product_schema: SaveProductSchema
    ) -> ProductSchema:
        product: Product = await self.product_repository.find_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )
        
        product_model = self.convert_schema_to_model(product_schema)

        product.category_id = product_model.category_id
        product.title = product_model.title
        product.cost = product_model.cost
        product.shipping_cost = product_model.shipping_cost
        product.currency_code = product_model.currency_code
        product.margin_percentage = product_model.margin_percentage
        product.main_image_url = product_model.main_image_url

        try:
            new_product = await self.product_repository.update(product)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid request body'
            )

        return new_product
    

    async def delete(self, product_id: UUID) -> None:
        product = await self.product_repository.find_by_id(product_id)

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )

        await self.product_repository.delete(product)


    @staticmethod
    def convert_schema_to_model(product_schema: SaveProductSchema) -> Product:
        return Product(
            category_id = product_schema.category_id,
            title = product_schema.title,
            cost = product_schema.cost,
            shipping_cost = product_schema.shipping_cost,
            currency_code = product_schema.currency_code,
            margin_percentage = product_schema.margin_percentage,
            main_image_url = str(product_schema.main_image_url)
        )