import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
DOKER_DATABASE_URL = os.getenv('DATABASE_URL')
LOCAL_DATABASE_URL = 'postgresql+asyncpg://postgres:posrgres@0.0.0.0:5432/postgres'

engine = create_async_engine(
    LOCAL_DATABASE_URL,
)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

async def get_db():
    async with SessionLocal() as db:
        yield db

async def create_tables():
    engine = create_async_engine(LOCAL_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# async def drop_tables():
#     engine = create_async_engine(LOCAL_DATABASE_URL)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
