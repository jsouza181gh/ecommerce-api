from dataclasses import dataclass
from fastapi import HTTPException, status
from datetime import datetime, UTC
from uuid import UUID
import bcrypt

from ..repositories import UserRepository, RoleRepository, RefreshTokenRepository
from ..schemas import SaveUserSchema, LoginSchema, AuthTokenSchema
from ..services import TokenService
from ..models import User

from config import DEFAULT_ROLE

@dataclass
class AuthService:
    user_repository: UserRepository
    role_repository: RoleRepository
    token_repository: RefreshTokenRepository
    token_service: TokenService

    async def register(self, user_schema: SaveUserSchema) -> AuthTokenSchema:
        email_exists = await self.user_repository.exists_by_email(user_schema.email)

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this e-mail already exists'
            )
        
        role_id = await self.default_role_id()
        hashed_password = self.hash_password(user_schema.password)

        new_user = self.convert_schema_to_model(
            user_schema,
            role_id,
            hashed_password
        )

        try:
            await self.user_repository.create(new_user)

        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not user due to data conflict'
            )
        
        access_token = self.token_service.generate_access_token(
            new_user.id,
            new_user.role
        )

        refresh_token = self.token_service.generate_refresh_token(new_user.id)

        try:
            await self.token_repository.create(refresh_token)

        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not token due to data conflict'
            )
        
        return AuthTokenSchema(
            access_token=access_token,
            refresh_token=refresh_token.token
        )


    async def login(self, login_schema: LoginSchema) -> AuthTokenSchema:
        user = await self.user_repository.find_by_email(login_schema.email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='E-mail or password is incorrect'
            )

        valid_password = bcrypt.checkpw(
            login_schema.password.encode(),
            user.password.encode()
        )

        if not valid_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='E-mail or password is incorrect'
            )

        access_token = self.token_service.generate_access_token(
            user.id,
            user.role
        )

        refresh_token = self.token_service.generate_refresh_token(user.id)

        old_token = await self.token_repository.find_by_user_id(user.id)

        if old_token:
            old_token.revoked = True
            await self.token_repository.update(old_token)

        try:
            await self.token_repository.create(refresh_token)

        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not token due to data conflict'
            )

        return AuthTokenSchema(
            access_token=access_token,
            refresh_token=refresh_token.token
        )


    async def logout(self, token_schema: AuthTokenSchema) -> None:
        refresh_token = await self.token_repository.find_by_value(token_schema.refresh_token)

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token'
            )

        decoded_token = self.token_service.decode_access_token(token_schema.access_token)
        user_id = UUID(decoded_token.sub)

        if user_id != refresh_token.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token'
            )

        refresh_token.revoked = True

        try:
            await self.token_repository.update(refresh_token)

        except:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Could not token due to data conflict'
            )


    async def refresh_token(self, token_schema: AuthTokenSchema) -> str:
        refresh_token = await self.token_repository.find_by_value(token_schema.refresh_token)

        if not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token'
            )

        is_expired = refresh_token.expires_at < datetime.now(UTC)

        if is_expired:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Expired refresh token'
            )

        decoded_token = self.token_service.decode_access_token(token_schema.access_token)
        user_id = UUID(decoded_token.sub)

        if user_id != refresh_token.user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh token'
            )

        access_token = self.token_service.generate_access_token(
            user_id,
            decoded_token.role
        )

        return access_token
    
    async def deactivate(self, user_id: UUID) -> None:
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        user.is_active = False

        await self.user_repository.update(user)

    
    async def default_role_id(self) -> UUID:
        default_role = await self.role_repository.find_by_name(DEFAULT_ROLE)

        if not default_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Customer role has not been configured'
            )
        
        return default_role.id


    @staticmethod
    def convert_schema_to_model(
        user_schema: SaveUserSchema,
        role_id: UUID,
        hashed_password: str
    ) -> User:
        return User(
            role_id=role_id,
            email=user_schema.email,
            first_name=user_schema.first_name,
            password=hashed_password,
            last_name=user_schema.last_name,
            is_active=True
        )
    

    @staticmethod
    def hash_password(password: str) -> str:
        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )
        return hashed_password.decode()