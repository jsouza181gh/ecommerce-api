from sqlalchemy.ext.asyncio import create_async_engine
from app.config import DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20
)