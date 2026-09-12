from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID

class AuthTokenSchema(BaseModel):
    access_token: str
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)


class SaveRefreshTokenSchema(BaseModel):
    user_id: UUID
    token: str
    created_at: datetime
    expires_at: datetime


class RefreshTokenSchema(BaseModel):
    id: UUID
    user_id: UUID
    token: str
    revoked: bool
    created_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)