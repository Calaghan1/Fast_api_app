import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app, reverse

client = TestClient(app)


menu = {'title': 'menu 1', 'description': 'desc 1'}
menu_update = {'title': 'update menu 1', 'description': 'update desc 1'}

menu_id = ''
# from database.database import get_db


# async def create_table():
#     engine = create_async_engine(END_URL)
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def test_get_menu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_menu'))
        assert response.status_code == 200
        assert response.json() == [], 'Fail'


@pytest.mark.asyncio
async def test_create_menu():
    global menu_id
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post(reverse('create_menu'), json=menu)
        assert response.status_code == 201
        response = response.json()
        assert response['title'] == menu['title']
        assert response['description'] == menu['description']
        menu_id = str(response['id'])


@pytest.mark.asyncio
async def test_get_uniq_menu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_uniq_menu', {'target_menu_id': menu_id}))
        assert response.status_code == 200, 'Fail'
        response = response.json()
        assert response['title'] == menu['title']
        assert response['description'] == menu['description']


@pytest.mark.asyncio
async def test_update_menu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.patch(reverse('update_menu', {'target_menu_id': menu_id}), json=menu_update)
        assert response.status_code == 200
        response = response.json()
        assert response['title'] == menu_update['title']
        assert response['description'] == menu_update['description']


@pytest.mark.asyncio
async def test_delete_menu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.delete(reverse('delete_menu', {'target_menu_id': menu_id}))
        assert response.status_code == 200
        assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


@pytest.mark.asyncio
async def test_get_deleted():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_menu'))
        assert response.status_code == 200, 'Fail'
        assert response.json() == [], 'Fail'
