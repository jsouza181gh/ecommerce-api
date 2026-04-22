from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List
from uuid import UUID

from ..repositories import ProductImageRepository, ProductRepository
from ..schemas import SaveProductImageSchema, ProductImageSchema
from ..models import ProductImage

@dataclass
class ProductImageService:
    image_repository: ProductImageRepository
    product_repository: ProductRepository

    async def create(self, image_schema: SaveProductImageSchema) -> ProductImageSchema:
        product_exists = await self.product_repository.exists(image_schema.product_id)

        if not product_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product was not found'
            )

        max_position = await self.image_repository.get_max_position(image_schema.product_id)

        if not max_position:
            max_position = 0

        new_image = self.convert_schema_to_model(image_schema, max_position)

        try:
            await self.image_repository.create(new_image)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not create product image due to data conflict'
            )

        return ProductImageSchema.model_validate(new_image)


    async def find_by_id(self, image_id: UUID) -> ProductImageSchema:
        image = await self.image_repository.find_by_id(image_id)

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Image was not found'
            )
        
        return ProductImageSchema.model_validate(image)


    async def find_all(self) -> List[ProductImageSchema]:
        images = await self.image_repository.find_all()
        
        return [
            ProductImageSchema.model_validate(image)
            for image in images
        ]


    async def update(
        self,
        image_id: UUID,
        image_schema: SaveProductImageSchema
    ) -> ProductImageSchema:
        image: ProductImage = await self.image_repository.find_by_id(image_id)

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Image was not found'
            )

        image_model = self.convert_schema_to_model(image_schema)

        image.product_id = image_model.product_id
        image.title = image_model.title
        image.image_url = image_model.image_url

        try:
            new_image = await self.image_repository.update(image)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid request body'
            )

        return ProductImageSchema.model_validate(new_image)


    async def delete(self, image_id: UUID) -> None:
        image = await self.image_repository.find_by_id(image_id)

        if not image_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Image was not found'
            )
        
        await self.image_repository.delete(image)


    @staticmethod
    def convert_schema_to_model(image_schema: SaveProductImageSchema, position: int = 0) -> ProductImage:
        if position:
            position += 1

        return ProductImage(
            product_id=image_schema.product_id,
            title=image_schema.title,
            image_url=str(image_schema.image_url),
            position=position
        )