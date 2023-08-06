from fastapi.testclient import TestClient

from app.main import app, reverse

client = TestClient(app)

menu = {'title': 'menu 1', 'description': 'desc 1'}
submenu = {'title': 'submenu 1', 'description': 'sub desc 1'}
updated_submenu = {'title': 'updated submenu 1', 'description': ' updated sub desc 1'}
menu_id = ''
submenu_id = ' '
# def test_drop_tables():
#     models.Menu.__table__.drop()


def test_create_test_menu():
    global menu_id
    response = client.post(reverse('create_menu'), json=menu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']
    menu_id = str(response['id'])
    print(menu_id)


def test_get_submenu():
    response = client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_create_submenu():
    global submenu_id
    reverse('create_submenu', {'target_menu_id': menu_id})
    response = client.post(reverse('create_submenu', {'target_menu_id': menu_id}), json=submenu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']
    submenu_id = str(response['id'])


def test_get_submenu_1():
    response = client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response[0]['title'] == submenu['title']
    assert response[0]['description'] == submenu['description']


def test_get_uniq_submenu():
    response = client.get(reverse('get_uniq_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']


def test_update_submenu():
    response = client.patch(
        reverse('update_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}), json=updated_submenu)
    assert response.status_code == 200
    response = response.json()
    assert response['title'] == updated_submenu['title']
    assert response['description'] == updated_submenu['description']


def test_get_uniq_submenu_1():
    response = client.get(reverse('get_uniq_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == updated_submenu['title']
    assert response['description'] == updated_submenu['description']


def test_delete_submenu():
    response = client.delete(reverse('delete_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


def test_get_submenu_1_1():
    response = client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_delete_menu_1():
    response = client.delete(reverse('delete_menu', {'target_menu_id': menu_id}))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


def test_get_deleted():
    response = client.get(reverse('get_menu'))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'
