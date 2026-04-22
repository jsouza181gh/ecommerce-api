from sqlalchemy.orm import declarative_base
from .engine import engine

Base = declarative_base()

from modules.product.models import *

async def createDataBase(drop_all: bool):
    async with engine.begin() as conn:
        if drop_all:
            await conn.run_sync(Base.metadata.drop_all)
            
        await conn.run_sync(Base.metadata.create_all)