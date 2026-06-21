from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class SaveUserSchema(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str


class UserSchema(BaseModel):
    id: UUID
    role_id: UUID
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)