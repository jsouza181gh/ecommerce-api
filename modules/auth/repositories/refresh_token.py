from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from uuid import UUID

from ..models import RefreshToken

@dataclass
class RefreshTokenRepository:
    session: AsyncSession

    async def create(self, token: RefreshToken) -> RefreshToken:
        self.session.add(token)
        await self.session.flush()

        return token


    async def find_by_value(self, token_value: str) -> RefreshToken:
        query = (
            select(RefreshToken)
            .where(RefreshToken.token == token_value)
        )

        return await self.session.scalar(query)


    async def update(self, token: RefreshToken) -> RefreshToken:
        await self.session.flush()

        return token


    async def revoke_old_tokens(self, user_id: UUID) -> None:
        query = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id==user_id,
                RefreshToken.revoked==False
            )
            .values(revoked=True)
        )

        await self.session.execute(query)
        await self.session.flush()


    async def delete(self, token: RefreshToken) -> None:
        await self.session.delete(token)