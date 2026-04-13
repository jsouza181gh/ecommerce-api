from pydantic import BaseModel, AnyUrl
from decimal import Decimal
from uuid import UUID

class SaveProductSchema(BaseModel):
    category_id: UUID
    title: str
    cost: Decimal
    shipping_cost: Decimal
    currency_code: str
    margin_percentage: Decimal
    main_image_url: AnyUrl

class ProductSchema(BaseModel):
    id: UUID
    category_id: UUID
    title: str
    cost: Decimal
    shipping_cost: Decimal
    currency_code: str
    margin_percentage: Decimal
    main_image_url: AnyUrl