from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Sequence
from uuid import UUID

from ..models import Role

@dataclass
class RoleRepository:
    session: AsyncSession

    async def find_by_id(self, role_id: UUID) -> Optional[Role]:
        return await self.session.get(
            Role,
            role_id
        )


    async def find_by_name(self, role_name: str) -> Optional[Role]:
        query = (
            select(Role)
            .where(Role.name == role_name)
        )
        
        return await self.session.scalar(query)


    async def find_all(self) -> Sequence[Role]:
        results = await self.session.scalars(
            select(Role)
        )

        return results.all()