from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from sqlalchemy.orm import selectinload
from typing import Optional, Sequence
from uuid import UUID

from ..models import User

@dataclass
class UserRepository:
    session: AsyncSession

    async def create(self, new_user: User) -> User:
        self.session.add(new_user)
        await self.session.flush()

        return new_user

    
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.session.get(
            User,
            user_id
        )
    

    async def find_by_email(self, user_email: str) -> Optional[User]:
        query = (
            select(User)
            .options(selectinload(User.role))
            .where(User.email == user_email)
        )

        return await self.session.scalar(query)


    async def find_all(self) -> Sequence[User]:
        results = await self.session.scalars(
            select(User)
        )
        
        return results.all()


    async def update(self, user: User) -> User:
        await self.session.flush()

        return user


    async def delete(self, user: User) -> None:
        await self.session.delete(user)


    async def exists(self, user_id: UUID) -> bool:
        query = select(
            exists()
            .where(User.id == user_id)
        )

        result = await self.session.scalar(query)
        return bool(result)
    

    async def exists_by_email(self, user_email: str) -> bool:
        query = select(
            exists()
            .where(User.email == user_email)
        )
        
        result = await self.session.scalar(query)
        return bool(result)