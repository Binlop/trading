from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import DateTime, func
from core.config import settings
from datetime import datetime

async_engine = create_async_engine(settings.DATABASE_URL)

LocalSession = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)

class Base(DeclarativeBase):
    created_on: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_on: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

async def get_async_db():
    async with LocalSession() as session:
        yield session