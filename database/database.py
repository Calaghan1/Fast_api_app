import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DOKER_DATABASE_URL = os.getenv('DATABASE_URL')

LOCAL_DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/postgres'
END_URL = ''

if DOKER_DATABASE_URL:
    END_URL = DOKER_DATABASE_URL
else:
    END_URL = LOCAL_DATABASE_URL

engine = create_async_engine(
    DOKER_DATABASE_URL,
)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db


async def create_tables():
    engine = create_async_engine(DOKER_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
