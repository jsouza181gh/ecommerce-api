from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from typing import Optional, List
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
        return await self.session.get(ProductCategory, category_id)
    
    
    async def exists(self, category_id: UUID) -> bool:
        query = select(
            exists().where(ProductCategory.id == category_id)
        )

        result = await self.session.scalar(query)
        return bool(result)


    async def find_all(self, name: Optional[str]) -> List[ProductCategory]:
        query = select(ProductCategory)

        if name:
            query = query.where(ProductCategory.name.ilike(f'%{name}%'))

        result = await self.session.execute(query)
        return result.scalars().all()
    

    async def update(self, category: ProductCategory) -> ProductCategory:
        await self.session.flush()

        return category
    
    
    async def delete(self, category: ProductCategory) -> None:
        await self.session.delete(category)