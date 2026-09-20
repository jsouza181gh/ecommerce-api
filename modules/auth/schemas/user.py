from pydantic import BaseModel, ConfigDict, EmailStr    
from datetime import datetime
from uuid import UUID

class SaveUserSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserSchema(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)