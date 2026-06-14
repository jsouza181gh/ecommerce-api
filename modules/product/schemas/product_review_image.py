from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class SaveProductReviewImageSchema(BaseModel):
    review_id: UUID
    title: Optional[str]
    image_url: str


class ProductReviewImageSchema(BaseModel):
    id: UUID
    review_id: UUID
    title: Optional[str]
    image_url: str
    position: int