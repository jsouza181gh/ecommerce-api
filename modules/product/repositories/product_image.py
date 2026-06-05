from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func
from typing import Optional, Sequence
from uuid import UUID

from ..models import ProductImage

@dataclass
class ProductImageRepository:
    session: AsyncSession

    async def create(self, new_image: ProductImage) -> ProductImage:
        self.session.add(new_image)
        await self.session.flush()

        return new_image


    async def find_by_id(self, image_id: UUID) -> Optional[ProductImage]:
        return await self.session.get(ProductImage, image_id)
    

    async def get_max_position(self, product_id: UUID) -> Optional[int]:
        query = (
            select(func.max(ProductImage.position))
            .where(ProductImage.product_id == product_id)
        )

        return await self.session.scalar(query)


    async def exists(self, image_id: UUID) -> bool:
        query = select(
            exists()
            .where(ProductImage.id == image_id)
        )

        result = await self.session.execute(query)
        
        return bool(result)


    async def find_all(self) -> Sequence[ProductImage]:
        result = await self.session.execute(
            select(ProductImage)
        )
        
        return result.scalars().all()


    async def update(self, new_image: ProductImage) -> ProductImage:
        await self.session.flush()

        return new_image


    async def delete(self, image: ProductImage) -> None:
        await self.session.delete(image)