from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from typing import Optional, Sequence
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
    
    
    async def exists(self, product_id: UUID) -> bool:
        query = select(
            exists().where(Product.id == product_id)
        )

        result = await self.session.scalar(query)

        return bool(result)

    
    async def find_all(self) -> Sequence[Product]:
        result = await self.session.execute(select(Product))

        return result.scalars().all()
    

    async def update(self, product: Product) -> Product:
        await self.session.flush()

        return product
    

    async def delete(self, product: Product) -> None:
        await self.session.delete(product)