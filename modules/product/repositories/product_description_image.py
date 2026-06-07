from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func
from typing import Optional, Sequence
from uuid import UUID

from ..models import ProductDescriptionImage

@dataclass
class ProductDescriptionImageRepository:
    session: AsyncSession

    async def create(self, description_image: ProductDescriptionImage) -> ProductDescriptionImage:
        self.session.add(description_image)
        await self.session.flush()

        return description_image


    async def find_by_id(self, description_image_id: UUID) -> ProductDescriptionImage:
        return await self.session.get(
            ProductDescriptionImage,
            description_image_id
        )


    async def find_all(self) -> Sequence[ProductDescriptionImage]:
        results = await self.session.scalars(
            select(ProductDescriptionImage)
        )

        return results.all()


    async def update(self, description_image: ProductDescriptionImage) -> ProductDescriptionImage:
        await self.session.flush()

        return description_image


    async def delete(self, description_image: ProductDescriptionImage) -> None:
        await self.session.delete(description_image)


    async def exists(self, description_image_id: UUID) -> bool:
        query = select(
            exists()
            .where(ProductDescriptionImage.id == description_image_id)
        )

        result = await self.session.scalar(query)
        return bool(result)


    async def get_max_position(self, description_section_id: UUID) -> Optional[int]:
        query = (
            select(func.max(ProductDescriptionImage.position))
            .where(ProductDescriptionImage.description_section_id == description_section_id)
        )

        return await self.session.scalar(query)