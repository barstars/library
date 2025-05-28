from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import setting

from typing import AsyncGenerator

engine = create_async_engine(setting.DATABASE_URL)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

from typing import AsyncGenerator

async def get_db() -> AsyncGenerator:
	"""
	Submits a session for the database
	"""
    async with SessionLocal() as session:
        yield session