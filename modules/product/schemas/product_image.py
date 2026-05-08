from pydantic import BaseModel, AnyUrl, ConfigDict
from uuid import UUID

class SaveProductImageSchema(BaseModel):
    product_id: UUID
    title: str
    image_url: AnyUrl

class ProductImageSchema(BaseModel):
    id: UUID
    product_id: UUID
    title: str
    image_url: AnyUrl
    position: int

    model_config = ConfigDict(from_attributes=True)