from sqlalchemy.ext.asyncio import async_sessionmaker
from .engine import engine

Session = async_sessionmaker(
    bind=engine, 
    expire_on_commit=False
)

async def get_database():
    async with Session() as session:
        try:
            yield session
            await session.commit()

        except Exception:
            await session.rollback()
            raise