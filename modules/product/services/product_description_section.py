from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
from uuid import UUID

from ..schemas import SaveProductDescriptionSectionSchema, ProductDescriptionSectionSchema
from ..repositories import ProductDescriptionSectionRepository, ProductRepository
from ..models import ProductDescriptionSection

@dataclass
class ProductDescriptionSectionService:
    description_repository: ProductDescriptionSectionRepository
    product_repository: ProductRepository

    async def create(self, section_schema: SaveProductDescriptionSectionSchema) -> ProductDescriptionSectionSchema:
        product_exists = await self.product_repository.exists(section_schema.product_id)

        if not product_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product was not found'
            )
        
        max_position = await self.description_repository.get_max_position(section_schema.product_id)

        if max_position is not None:
            max_position += 1

        new_section = self.convert_schema_to_model(section_schema, max_position)

        try:
            await self.description_repository.create(new_section)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not create description section due to data conflict'
            )

        return ProductDescriptionSectionSchema.model_validate(new_section)


    async def find_by_id(self, section_id: UUID) -> ProductDescriptionSectionSchema:
        description_section = await self.description_repository.find_by_id(section_id)

        if not description_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description section was not found'
            )
        
        return ProductDescriptionSectionSchema.model_validate(description_section)


    async def find_all(self) -> List[ProductDescriptionSectionSchema]:
        description_sections = await self.description_repository.find_all()

        return [
            ProductDescriptionSectionSchema.model_validate(section)
            for section in description_sections
        ]


    async def update(
        self,
        section_id: UUID,
        section_schema: SaveProductDescriptionSectionSchema
    ) -> ProductDescriptionSectionSchema:
        description_section = await self.description_repository.find_by_id(section_id)

        if not description_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description section was not found'
            )
        
        section_model = self.convert_schema_to_model(section_schema, description_section.position)

        description_section.title = section_model.title
        description_section.subtitle = section_model.subtitle
        description_section.description = section_model.description
        
        return ProductDescriptionSectionSchema.model_validate(description_section)


    async def delete(self, section_id: UUID) -> None:
        description_section = await self.description_repository.find_by_id(section_id)

        if not description_section:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Description section was not found'
            )
        
        await self.description_repository.delete(description_section)


    @staticmethod
    def convert_schema_to_model(
        section_schema: SaveProductDescriptionSectionSchema,
        position: Optional[int] = 0
    ) -> ProductDescriptionSection:
 
        return ProductDescriptionSection(
            product_id=section_schema.product_id,
            title=section_schema.title,
            subtitle=section_schema.subtitle,
            description=section_schema.description,
            position=position
        )