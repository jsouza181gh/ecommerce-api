from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List
from uuid import UUID

from ..repositories import UserRepository
from ..schemas import SaveUserSchema, UserSchema
from ..models import User

@dataclass
class UserService:
    user_repository: UserRepository

    async def find_by_id(self, user_id: UUID) -> UserSchema:
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        return UserSchema.model_validate(user)


    async def find_all(self) -> List[UserSchema]:
        users = await self.user_repository.find_all()

        return [
            UserSchema.model_validate(user)
            for user in users
        ]


    async def update(self, user_id: UUID, user_schema: SaveUserSchema) -> UserSchema:
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )

        user_model = self.convert_schema_to_model(user_schema, user.role_id, user.password)

        user.email = user_model.email
        user.first_name = user_model.first_name
        user.last_name = user_model.last_name

        try:
            new_user = await self.user_repository.update(user)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid request body'
            )

        return UserSchema.model_validate(new_user)


    async def deactivate(self, user_id: UUID) -> None:
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        user.is_active = False

        await self.user_repository.update(user)


    async def delete(self, user_id: UUID) -> None:
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        await self.user_repository.delete(user)

    @staticmethod
    def convert_schema_to_model(
        user_schema: SaveUserSchema,
        role_id: UUID,
        password: str
    ) -> User:

        return User(
            role_id=role_id,
            email=user_schema.email,
            first_name=user_schema.first_name,
            password=password,
            last_name=user_schema.last_name,
            is_active=True
        )