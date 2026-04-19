from dataclasses import dataclass
from sqlalchemy.ext.asyncio import AsyncSession

@dataclass
class ProductImageRepository:
    db: AsyncSession

    async def create():
        pass


    async def find_by_id():
        pass


    async def exists():
        pass


    async def find_all():
        pass


    async def update():
        pass


    async def delete():
        pass