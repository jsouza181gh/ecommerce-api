from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func
from typing import Optional, Sequence
from uuid import UUID

from ..models import ProductDescriptionSection

@dataclass
class ProductDescriptionSectionRepository:
    session: AsyncSession

    async def create(self, new_section: ProductDescriptionSection) -> ProductDescriptionSection:
        self.session.add(new_section)
        await self.session.flush()

        return new_section


    async def find_by_id(self, section_id: UUID) -> Optional[ProductDescriptionSection]:
        return await self.session.get_one(ProductDescriptionSection, section_id)


    async def get_max_position(self, product_id: UUID) -> Optional[int]:
        query = (
            select(func.max(ProductDescriptionSection.position))
            .where(ProductDescriptionSection.product_id == product_id)
        )

        return await self.session.scalar(query)


    async def exists(self, section_id: UUID) -> bool:
        query = select(
            exists()
            .where(ProductDescriptionSection.id == section_id)
        )

        result = await self.session.execute(query)
        
        return bool(result)


    async def find_all(self) -> Sequence[ProductDescriptionSection]:
        result = await self.session.execute(
            select(ProductDescriptionSection)
        )

        return result.scalars().all()


    async def update(self, new_section: ProductDescriptionSection) -> ProductDescriptionSection:
        await self.session.flush()

        return new_section


    async def delete(self, section: ProductDescriptionSection) -> None:
        await self.session.delete(section)