from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.constants import settings


_engine = create_async_engine(
    url=settings.db.URL,
    connect_args={"server_settings": {"search_path": settings.db.SCHEMA}},
    echo=False,
    echo_pool=False,
)

_sessionmaker = async_sessionmaker(
    bind=_engine,
    autocommit=False,
    expire_on_commit=False,
)

_metadata = MetaData(schema=settings.db.SCHEMA)


class BaseORM(DeclarativeBase):
    metadata = _metadata


async def _get_session() -> AsyncGenerator[AsyncSession, None]:
    async with _sessionmaker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmaker_cm = asynccontextmanager(_get_session)
