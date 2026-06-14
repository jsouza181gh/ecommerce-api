from dataclasses import dataclass
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from uuid import UUID

from ..repositories import ProductReviewImageRepository, ProductReviewRepository
from ..schemas import SaveProductReviewImageSchema, ProductReviewImageSchema
from ..models import ProductReviewImage

@dataclass
class ProductReviewImageService:
    review_image_repository: ProductReviewImageRepository
    review_repository: ProductReviewRepository

    async def create(self, review_image_schema: SaveProductReviewImageSchema) -> ProductReviewImageSchema:
        review_exists = await self.review_repository.exists(review_image_schema.review_id)

        if not review_exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review was not found'
            )

        max_position = await self.review_image_repository.get_max_position(review_image_schema.review_id)

        if max_position is not None:
            max_position += 1

        new_review_image = self.convert_schema_to_model(review_image_schema, max_position)

        try:
            await self.review_image_repository.create(new_review_image)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not create review image due to data conflict'
            )

        return ProductReviewImageSchema.model_validate(new_review_image)


    async def find_by_id(self, review_image_id: UUID) -> ProductReviewImageSchema:
        review_image = await self.review_image_repository.find_by_id(review_image_id)

        if not review_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review image was not found'
            )

        return ProductReviewImageSchema.model_validate(review_image)


    async def find_all(self) -> List[ProductReviewImageSchema]:
        review_images = await self.review_image_repository.find_all()

        return [
            ProductReviewImageSchema.model_validate(review_image)
            for review_image in review_images
        ]


    async def update(self,
        review_image_id: UUID,
        review_image_schema: SaveProductReviewImageSchema
    ) -> ProductReviewImageSchema:
        review_image = await self.review_image_repository.find_by_id(review_image_id)

        if not review_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review image was not found'
            )

        review_image_model = self.convert_schema_to_model(review_image_schema)

        review_image.title = review_image_model.title
        review_image.image_url = review_image_model.image_url

        try:
            new_review_image = await self.review_image_repository.update(review_image)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid request body'
            )

        return ProductReviewImageSchema.model_validate(new_review_image)


    async def delete(self, review_image_id: UUID) -> None:
        review_image = await self.review_image_repository.find_by_id(review_image_id)

        if not review_image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Review image was not found'
            )

        await self.review_image_repository.delete(review_image)


    @staticmethod
    def convert_schema_to_model(
        review_image_schema: SaveProductReviewImageSchema,
        position: Optional[int] = 0
    ) -> ProductReviewImage:
        
        return ProductReviewImage(
            review_id=review_image_schema.review_id,
            title=review_image_schema.title,
            image_url=str(review_image_schema.image_url),
            position=position
        )