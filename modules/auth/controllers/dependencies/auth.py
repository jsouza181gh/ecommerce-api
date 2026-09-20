from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from infrastructure.database.session import get_database
from ...repositories import RefreshTokenRepository, UserRepository, RoleRepository
from ...services import TokenService, AuthService
from ...schemas import AuthTokensName
from ...models import User
from .user import get_user_repository

AccessToken =  Annotated[str, Depends(AuthService.get_required_cookie(AuthTokensName.ACCESS_TOKEN))]
RefreshToken =  Annotated[str, Depends(AuthService.get_required_cookie(AuthTokensName.REFRESH_TOKEN))]

def get_token_repository(db: Annotated[AsyncSession, Depends(get_database)]) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)

def get_role_repository(db: Annotated[AsyncSession, Depends(get_database)]) -> RoleRepository:
    return RoleRepository(db)

def get_token_service() -> TokenService:
    return TokenService()

def get_auth_service(
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    role_repository: Annotated[RoleRepository, Depends(get_role_repository)],
    token_repository: Annotated[RefreshTokenRepository, Depends(get_token_repository)],
    token_service: Annotated[TokenService, Depends(get_token_service)]
) -> AuthService:
    return AuthService(user_repository, role_repository, token_repository, token_service)

async def get_current_user(
    access_token: AccessToken,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> User:
    return await auth_service.get_current_user(access_token)

CurrentUser = Annotated[User, Depends(get_current_user)]

AuthDependencies = Annotated[
    AuthService,
    Depends(get_auth_service)
]