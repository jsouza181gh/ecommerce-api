from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from infrastructure.database.session import get_database
from ...repositories import UserRepository
from ...services import UserService

def get_user_repository(db: Annotated[AsyncSession, Depends(get_database)]) -> UserRepository:
    return UserRepository(db)

def get_user_service(user_repository: Annotated[UserRepository, Depends(get_user_repository)]) -> UserService:
    return UserService(user_repository)

UserDependencies = Annotated[
    UserService,
    Depends(get_user_service)
]