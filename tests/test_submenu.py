import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app, reverse

client = TestClient(app)


menu = {'title': 'menu 1', 'description': 'desc 1'}
submenu = {'title': 'submenu 1', 'description': 'sub desc 1'}
updated_submenu = {'title': 'updated submenu 1', 'description': ' updated sub desc 1'}
menu_id = ''
submenu_id = ' '
# async def test_drop_tables():
#     models.Menu.__table__.drop()


@pytest.mark.asyncio
async def test_create_test_menu():
    global menu_id
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post(reverse('create_menu'), json=menu)
        assert response.status_code == 201
        response = response.json()
        assert response['title'] == menu['title']
        assert response['description'] == menu['description']
        menu_id = str(response['id'])


@pytest.mark.asyncio
async def test_get_submenu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
        assert response.status_code == 200, 'Fail'
        assert response.json() == [], 'Fail'


@pytest.mark.asyncio
async def test_create_submenu():
    global submenu_id
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.post(reverse('create_submenu', {'target_menu_id': menu_id}), json=submenu)
        assert response.status_code == 201
        response = response.json()
        assert response['title'] == submenu['title']
        assert response['description'] == submenu['description']
        submenu_id = str(response['id'])


@pytest.mark.asyncio
async def test_get_submenu_1():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
        assert response.status_code == 200, 'Fail'
        response = response.json()
        assert response[0]['title'] == submenu['title']
        assert response[0]['description'] == submenu['description']


@pytest.mark.asyncio
async def test_get_uniq_submenu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_uniq_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
        assert response.status_code == 200, 'Fail'
        response = response.json()
        assert response['title'] == submenu['title']
        assert response['description'] == submenu['description']


@pytest.mark.asyncio
async def test_update_submenu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.patch(
            reverse('update_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}), json=updated_submenu)
        assert response.status_code == 200
        response = response.json()
        assert response['title'] == updated_submenu['title']
        assert response['description'] == updated_submenu['description']


@pytest.mark.asyncio
async def test_get_uniq_submenu_1():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_uniq_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
        assert response.status_code == 200, 'Fail'
        response = response.json()
        assert response['title'] == updated_submenu['title']
        assert response['description'] == updated_submenu['description']


@pytest.mark.asyncio
async def test_delete_submenu():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.delete(reverse('delete_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
        assert response.status_code == 200
        assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


@pytest.mark.asyncio
async def test_get_submenu_1_1():
    async with AsyncClient(app=app, base_url='http://test') as client:
        response = await client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
        assert response.status_code == 200, 'Fail'
        assert response.json() == [], 'Fail'


@pytest.mark.asyncio
async def test_delete_menu_1():
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
