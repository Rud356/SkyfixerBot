from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from Skyfixer.config import skyfixer_db_config

Base = declarative_base()
Session = sessionmaker(
    skyfixer_db_config.async_base_engine,
    expire_on_commit=False, class_=AsyncSession,
)
metadata = Base.metadata


async def drop_db():
    """
    Drops all tables in db.
    """
    async with skyfixer_db_config.async_base_engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


async def init_db():
    """
    Initialized all tables in db.
    """
    async with skyfixer_db_config.async_base_engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
