from pydantic import BaseModel, ConfigDict
from typing import Optional
from uuid import UUID

class SaveProductDescriptionSectionSchema(BaseModel):
    product_id: UUID
    title: str
    subtitle: Optional[str]
    description: str


class ProductDescriptionSectionSchema(BaseModel):
    id: UUID
    product_id: UUID
    title: str
    subtitle: Optional[str]
    description: str
    position: int

    model_config = ConfigDict(from_attributes=True)