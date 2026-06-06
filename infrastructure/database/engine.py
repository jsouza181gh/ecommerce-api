from sqlalchemy.ext.asyncio import create_async_engine

from config import DATABASE_URL

if not DATABASE_URL:
    raise RuntimeError('Database URL was not correctly defined')

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)