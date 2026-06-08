from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from typing import Optional, Sequence
from uuid import UUID

from ..models import ProductReview

@dataclass
class ProductReviewRepository:
    session: AsyncSession

    async def create(self, new_review: ProductReview) -> ProductReview:
        self.session.add(new_review)
        await self.session.flush()

        return new_review
    

    async def find_by_id(self, review_id: UUID) -> Optional[ProductReview]:
        return await self.session.get(
            ProductReview,
            review_id
        )
    

    async def find_all(self) -> Sequence[ProductReview]:
        results = await self.session.scalars(
            select(ProductReview)
        )

        return results.all()
    

    async def update(self, new_review: ProductReview) -> ProductReview:
        await self.session.flush()

        return new_review
    

    async def delete(self, review: ProductReview) -> None:
        await self.session.delete(review)


    async def exists(self, review_id: UUID) -> bool:
        query = select(
            exists()
            .where(ProductReview.id == review_id)
        )

        result = await self.session.scalar(query)
        return bool(result)