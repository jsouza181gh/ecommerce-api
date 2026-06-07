from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from uuid import UUID

from ..repositories import ProductDescriptionImageRepository, ProductDescriptionSectionRepository
from ..schemas import SaveProductDescriptionImageSchema, ProductDescriptionImageSchema
from ..models import ProductDescriptionImage

@dataclass
class ProductDescriptionImageService:
    description_image_repository: ProductDescriptionImageRepository
    description_section_repository: ProductDescriptionSectionRepository

    async def create(self, description_image_schema: SaveProductDescriptionImageSchema) -> ProductDescriptionImageSchema:
        description_section_exists = await self.description_section_repository.exists(description_image_schema.description_section_id)

        if not description_section_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description section was not found'
            )
        
        max_position = await self.description_image_repository.get_max_position(description_image_schema.description_section_id)

        if max_position is not None:
            max_position += 1

        description_image_model = self.convert_schema_to_model(description_image_schema, max_position)

        try:
            await self.description_image_repository.create(description_image_model)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not create description image due to data conflict'
            )

        return ProductDescriptionImageSchema.model_validate(description_image_model) 


    async def find_by_id(self, description_image_id: UUID) -> ProductDescriptionImageSchema:
        description_image = await self.description_image_repository.find_by_id(description_image_id)

        if not description_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description image was not found'
            )
        
        return ProductDescriptionImageSchema.model_validate(description_image)


    async def find_all(self) -> List[ProductDescriptionImageSchema]:
        description_images = await self.description_image_repository.find_all()

        return [
            ProductDescriptionImageSchema.model_validate(description_image)
            for description_image in description_images
        ]


    async def update(
        self,
        description_image_id: UUID,
        description_image_schema: SaveProductDescriptionImageSchema
    ) -> ProductDescriptionImageSchema:
        description_image = await self.description_image_repository.find_by_id(description_image_id)

        if not description_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description image was not found'
            )

        description_image_model = self.convert_schema_to_model(description_image_schema)

        description_image.title = description_image_model.title
        description_image.image_url = description_image_model.image_url

        try:
            new_description_image = await self.description_image_repository.update(description_image)

        except IndexError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid request body'
            )

        return ProductDescriptionImageSchema.model_validate(new_description_image)


    async def delete(self, description_image_id: UUID) -> None:
        description_image = await self.description_image_repository.find_by_id(description_image_id)

        if not description_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description image was not found'
            )

        await self.description_image_repository.delete(description_image)


    @staticmethod
    def convert_schema_to_model(
        description_image_schema: SaveProductDescriptionImageSchema,
        position: Optional[int] = 0
    ) -> ProductDescriptionImage:
        
        return ProductDescriptionImage(
            description_section_id=description_image_schema.description_section_id,
            title=description_image_schema.title,
            image_url=str(description_image_schema.image_url),
            position=position
        )                              