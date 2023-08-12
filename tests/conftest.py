import asyncio
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from database.database import get_db
from sqlalchemy import MetaData
from app.main import app
from database.database import Base, create_tables
# DOKER_DATABASE_URL = os.getenv('DATABASE_URL')
LOCAL_DATABASE_URL = 'postgresql+asyncpg://postgres:posrgres@0.0.0.0:5432/postgres'

# engine_test = create_async_engine(LOCAL_DATABASE_URL, poolclass=NullPool)
# async_session = sessionmaker(engine_test, class_=AsyncSession, expire_on_commit=False)
# # metadata = MetaData()
# # metadata.bind = engine_test

# async def test_get_db():
#     async with async_session as s:
#         yield s
        
# app.dependency_overrides[get_db] = test_get_db




    
@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()    
    
@pytest.fixture(scope='session')
async def ac():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac