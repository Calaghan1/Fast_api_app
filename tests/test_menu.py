from fastapi.testclient import TestClient

from app.main import app, reverse

client = TestClient(app)

menu = {'title': 'menu 1', 'description': 'desc 1'}
menu_update = {'title': 'update menu 1', 'description': 'update desc 1'}

menu_id = ''


def test_get_menu():
    response = client.get(reverse('get_menu'))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_create_menu():
    global menu_id
    response = client.post(reverse('create_menu'), json=menu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']
    menu_id = str(response['id'])


def test_get_uniq_menu():
    response = client.get(reverse('get_uniq_menu', {'target_menu_id': menu_id}))
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']


def test_update_menu():
    response = client.patch(reverse('update_menu', {'target_menu_id': menu_id}), json=menu_update)
    assert response.status_code == 200
    response = response.json()
    assert response['title'] == menu_update['title']
    assert response['description'] == menu_update['description']


def test_delete_menu():
    response = client.delete(reverse('delete_menu', {'target_menu_id': menu_id}))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


def test_get_deleted():
    response = client.get(reverse('get_menu'))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'
