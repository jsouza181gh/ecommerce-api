from pydantic import BaseModel, ConfigDict, AnyUrl
from typing import Optional
from uuid import UUID

class SaveProductDescriptionImageSchema(BaseModel):
    description_section_id: UUID
    title: Optional[str]
    image_url: AnyUrl

class ProductDescriptionImageSchema(BaseModel):
    id: UUID
    description_section_id: UUID
    title: Optional[str]
    image_url: AnyUrl
    position: int

    model_config = ConfigDict(from_attributes=True)