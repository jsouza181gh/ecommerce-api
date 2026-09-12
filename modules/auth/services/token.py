from dataclasses import dataclass
from datetime import datetime, timedelta, UTC
from uuid import UUID
from jose import jwt
import secrets

from ..schemas import JWTPayloadSchema
from ..models import RefreshToken

from config import JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

@dataclass
class TokenService:
    secret_key: str = JWT_SECRET_KEY
    algorithm: str =JWT_ALGORITHM
    jwt_expires: int = JWT_EXPIRE_MINUTES
    refresh_token_expires: int = REFRESH_TOKEN_EXPIRE_DAYS

    def generate_access_token(self, user_id: UUID, role: str) -> str:
        now = datetime.now(UTC)

        payload = JWTPayloadSchema(
            sub = str(user_id),
            role = role,
            iat= int(now.timestamp()),
            exp = int(
                (now + timedelta(minutes=self.jwt_expires))
                .timestamp()
            )
        )

        return jwt.encode(
            payload.model_dump(),
            self.secret_key,
            algorithm=self.algorithm
        )

    def generate_refresh_token(self, user_id: UUID) -> RefreshToken:
        token = secrets.token_urlsafe(64)
        created_at = datetime.now(UTC)
        expires_at = created_at + timedelta(days=self.refresh_token_expires)

        return RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )


    def decode_access_token(self, access_token: str) -> JWTPayloadSchema:
        decoded_token = jwt.decode(
            token=access_token,
            key=JWT_SECRET_KEY
        )

        return JWTPayloadSchema(
            sub=decoded_token['sub'],
            role=decoded_token['role'],
            iat=decoded_token['iat'],
            exp=decoded_token['exp'],
        )