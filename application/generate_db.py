import asyncio

from infrastructure.database import Base
from infrastructure.database.session import engine


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def truncate_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(create_database())
