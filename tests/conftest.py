from asyncio import get_event_loop
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from app.main import app
from database.database import SessionLocal


@pytest.fixture(scope='session')
def db() -> Generator:

    yield SessionLocal()


@pytest.fixture(scope='module')
async def async_client() -> AsyncGenerator:

    async with AsyncClient(app=app, base_url='http://testserver') as client:

        yield client


@pytest.fixture(scope='module')
def event_loop():

    loop = get_event_loop()

    yield loop
