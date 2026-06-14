from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func
from typing import Sequence, Optional
from uuid import UUID

from ..models import ProductReviewImage

@dataclass
class ProductReviewImageRepository:
    session: AsyncSession

    async def create(self, new_review_image: ProductReviewImage) -> ProductReviewImage:
        self.session.add(new_review_image)
        await self.session.flush()

        return new_review_image


    async def find_by_id(self, review_image_id: UUID) -> ProductReviewImage:
        return await self.session.get(
            ProductReviewImage,
            review_image_id
        )


    async def find_all(self) -> Sequence[ProductReviewImage]:
        results = await self.session.scalars(
            select(ProductReviewImage)
        )

        return results.all()


    async def update(self, review_image: ProductReviewImage) -> ProductReviewImage:
        await self.session.flush()
        
        return review_image


    async def delete(self, review_image: ProductReviewImage) -> None:
        await self.session.delete(review_image)


    async def exists(self, review_image_id: UUID) -> bool:
        query = select(
            exists()
            .where(ProductReviewImage.id == review_image_id)
        )

        result = await self.session.scalar(query)
        return bool(result)


    async def get_max_position(self, review_id: UUID) -> Optional[int]:
        query = (
            select(func.max(ProductReviewImage.position))
            .where(ProductReviewImage.review_id == review_id)
        )

        return await self.session.scalar(query)