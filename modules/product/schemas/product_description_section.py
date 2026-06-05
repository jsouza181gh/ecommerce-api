from pydantic import BaseModel, ConfigDict
from uuid import UUID

class SaveProductDescriptionSectionSchema(BaseModel):
    product_id: UUID
    title: str
    subtitle: str
    description: str


class ProductDescriptionSectionSchema(BaseModel):
    id: UUID
    product_id: UUID
    title: str
    subtitle: str
    descrition: str
    position: int

    model_config = ConfigDict(from_attributes=True)