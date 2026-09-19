from dataclasses import dataclass
from fastapi import HTTPException, status, Cookie
from jose import ExpiredSignatureError, JWTError
from typing import Annotated
from uuid import UUID
import bcrypt

from ..repositories import UserRepository, RoleRepository, RefreshTokenRepository
from ..schemas import SaveUserSchema, LoginSchema, AuthTokenSchema, RoleSchema
from ..services import TokenService
from ..models import User

from config import DEFAULT_ROLE

@dataclass
class AuthService:
    user_repository: UserRepository
    role_repository: RoleRepository
    token_repository: RefreshTokenRepository
    token_service: TokenService

    async def signup(self, user_schema: SaveUserSchema) -> AuthTokenSchema:
        email_exists = await self.user_repository.exists_by_email(user_schema.email)

        if email_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this e-mail already exists'
            )
        
        role = await self.default_role()
        hashed_password = self.hash_password(user_schema.password)

        new_user = self.convert_schema_to_model(
            user_schema,
            role.id,
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
            new_user.role.name
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


    async def signin(self, login_schema: LoginSchema) -> AuthTokenSchema:
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
            user.role.name
        )

        refresh_token = self.token_service.generate_refresh_token(user.id)

        await self.token_repository.revoke_old_tokens(user.id)

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


    async def signout(self, token_schema: AuthTokenSchema) -> None:
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


    async def get_current_user(self, token: str) -> User:
        try:
            decoded_token = self.token_service.decode_access_token(token)

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        user = await self.user_repository.find_by_id(UUID(decoded_token.sub))

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Unrecognized access token'
            )

        return user


    async def refresh(self, token_schema: AuthTokenSchema) -> AuthTokenSchema:        
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

        access_token = self.token_service.generate_access_token(
            user_id,
            decoded_token.role
        )

        return AuthTokenSchema(
            access_token=access_token,
            refresh_token=token_schema.refresh_token
        )

    
    async def default_role(self) -> RoleSchema:
        default_role = await self.role_repository.find_by_name(DEFAULT_ROLE)

        if not default_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='Customer role has not been configured'
            )
        
        return default_role


    @staticmethod
    def get_required_cookie(
        cookie_name: str
    ):
        def cookie_dependency(cookie: Annotated[str | None, Cookie(alias=cookie_name)] = None) -> Annotated[str, Cookie()]:
            if cookie is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Authentication required'
                )

            return cookie
        
        return cookie_dependency


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