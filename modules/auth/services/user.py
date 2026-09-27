from dataclasses import dataclass
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List
from uuid import UUID

from ..schemas import SaveUserSchema, UserSchema
from ..repositories import UserRepository
from ..models import User

@dataclass
class UserService:
    user_repository: UserRepository

    async def find_by_id(
        self,
        user_id: UUID,
        current_user: User
    ) -> UserSchema:
        has_permission = self.has_permission('read', current_user)
        is_current_user = user_id == current_user.id

        if not (has_permission and is_current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to access this resource'
            )
        
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        return UserSchema.model_validate(user)


    async def find_all(
        self,
        current_user: User
    ) -> List[UserSchema]:
        has_permission = self.has_permission("list", current_user)

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to access this resource'
            )

        users = await self.user_repository.find_all()

        return [
            UserSchema.model_validate(user)
            for user in users
        ]


    async def update(
        self,
        user_id: UUID,
        user_schema: SaveUserSchema,
        current_user: User
    ) -> UserSchema:
        has_permission = self.has_permission('update', current_user)
        is_current_user = user_id == current_user.id

        if not (has_permission and is_current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to access this resource'
            )
        
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
                detail='Email address is already in use'
            )

        return UserSchema.model_validate(new_user)


    async def activate(
        self,
        user_id: UUID,
        current_user: User
    ) -> None:
        has_permission = self.has_permission("activate", current_user)
        is_current_user = user_id == current_user.id

        if not (has_permission and is_current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to access this resource'
            )            

        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        user.is_active = True

        await self.user_repository.update(user)


    async def deactivate(
        self, 
        user_id: UUID,
        current_user: User
    ) -> None:
        has_permission = self.has_permission('deactivate', current_user)
        is_current_user = user_id == current_user.id

        if not (has_permission and is_current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to access this resource'
            )            

        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        user.is_active = False

        await self.user_repository.update(user)


    async def delete(
        self,
        user_id: UUID,
        current_user: User
    ) -> None:
        has_permission = self.has_permission('delete', current_user)

        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to access this resource'
            )
        
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User was not found'
            )
        
        await self.user_repository.delete(user)


    @staticmethod
    def has_permission(
        permission: str,
        current_user: User
    ) -> bool:
        user_permissions = current_user.role.permissions

        return any(
            user_permission.name == f"users:{permission}"
            for user_permission in user_permissions
        )


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