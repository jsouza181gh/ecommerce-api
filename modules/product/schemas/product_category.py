from pydantic import BaseModel
from uuid import UUID

class SaveProductCategorySchema(BaseModel):
    name: str

class ProductCategorySchema(BaseModel):
    id: UUID
    name: str