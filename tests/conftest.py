from main import app, get_session

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


engine = create_async_engine(
    url="postgresql+asyncpg://postgres:postgres@localhost:6432/postgres"
)


new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


# app.dependency_overrides[get_session] = 