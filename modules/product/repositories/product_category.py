from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from typing import Optional, Sequence
from uuid import UUID

from ..models import ProductCategory

@dataclass
class ProductCategoryRepository:
    session: AsyncSession

    async def create(self, category: ProductCategory) -> ProductCategory:
        self.session.add(category)
        await self.session.flush()

        return category


    async def find_by_id(self, category_id: UUID) -> ProductCategory:
        return await self.session.get(
            ProductCategory,
            category_id
        )


    async def find_all(self, search: Optional[str]) -> Sequence[ProductCategory]:
        query = select(ProductCategory)

        if search:
            query = query.where(ProductCategory.name.ilike(f'%{search}%'))

        results = await self.session.scalars(query)
        return results.all()


    async def update(self, category: ProductCategory) -> ProductCategory:
        await self.session.flush()

        return category


    async def delete(self, category: ProductCategory) -> None:
        await self.session.delete(category)


    async def exists(self, category_id: UUID) -> bool:
        query = select(
            exists()
            .where(ProductCategory.id == category_id)
        )

        result = await self.session.scalar(query)
        return bool(result)