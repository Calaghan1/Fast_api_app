from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

menu_id = ''
submenu_id = ''
dish_id = ''

menu = {'title': 'menu 1', 'description': 'desc 1'}
submenu = {'title': 'submenu 1', 'description': 'sub desc 1'}
dish = {
    'title': 'My dish 1',
    'description': 'My dish description 1',
    'price': '12.50'
}
dish_2 = {
    'title': 'My dish 2',
    'description': 'My dish description 2',
    'price': '32.50'
}

updated_dish = {
    'title': 'My updated dish 1',
    'description': 'My updated dish description 1',
    'price': '22.50'
}


def test_create_menu():
    response = client.post('/api/v1/menus', json=menu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']
    global menu_id
    menu_id = str(response['id'])


def test_create_submenu():
    global submenu_id
    response = client.post(f'/api/v1/menus/{menu_id}/submenus', json=submenu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']
    submenu_id = str(response['id'])


def test_create_dish():
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == dish['title']
    assert response['description'] == dish['description']
    global dish_id
    dish_id = str(response['id'])


def test_create_dish_1():
    response = client.post(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json=dish_2)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == dish_2['title']
    assert response['description'] == dish_2['description']
    global dish_id
    dish_id = str(response['id'])


def test_get_dishes_o():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response[0]['title'] == dish['title']
    assert response[0]['description'] == dish['description']
    assert response[1]['title'] == dish_2['title']
    assert response[1]['description'] == dish_2['description']


def test_get_uniq_menu():
    response = client.get(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']
    assert response['submenus_count'] == 1
    assert response['dishes_count'] == 2


def test_get_uniq_submenu():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']
    assert response['dishes_count'] == 2


def test_delete_submenu():
    response = client.delete(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


def test_get_submenu():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus')
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_get_dishes_o1():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes')
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response == []


def test_get_uniq_submenu_1():
    response = client.get(f'/api/v1/menus/{menu_id}/submenus/{submenu_id}')
    assert response.status_code == 404, 'Fail'


def test_delete_menu():
    response = client.delete(f'/api/v1/menus/{menu_id}')
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


def test_get_menu():
    response = client.get('/api/v1/menus')
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'
