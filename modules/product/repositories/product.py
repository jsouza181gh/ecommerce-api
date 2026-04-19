from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.sqltypes import String as SQLAlchemyString
from sqlalchemy import select, exists
from typing import Optional, List
from uuid import UUID

from ..models import Product

@dataclass
class ProductRepository:
    session: AsyncSession

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.flush()

        return product
    
    
    async def find_by_id(self, product_id: UUID) -> Optional[Product]:
        return await self.session.get(Product, product_id)
    
    
    async def exists(self, category_id: UUID) -> bool:
        query = select(
            exists().where(Product.id == category_id)
        )

        result = await self.session.scalar(query)

        return bool(result)

    
    async def find_all(self) -> List[Product]:
        result = await self.session.execute(select(Product))

        return result.scalars().all()
    

    async def update(self, product: Product) -> Product:
        await self.session.flush()

        return product
    

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)