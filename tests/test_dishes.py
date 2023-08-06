from fastapi.testclient import TestClient

from app.main import app, reverse

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
updated_dish = {
    'title': 'My updated dish 1',
    'description': 'My updated dish description 1',
    'price': '22.50'
}


def test_create_menu():
    response = client.post(reverse('create_menu'), json=menu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']
    global menu_id
    menu_id = str(response['id'])


def test_create_submenu():
    global submenu_id
    response = client.post(reverse('create_submenu', {'target_menu_id': menu_id}), json=submenu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']
    submenu_id = str(response['id'])


def test_get_dishes():
    response = client.get(reverse('get_dishes', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_create_dish():

    response = client.post(
        reverse('create_dish', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}), json=dish)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == dish['title']
    assert response['description'] == dish['description']
    global dish_id
    dish_id = str(response['id'])


def test_get_dishes_o():
    response = client.get(reverse('get_dishes', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response[0]['title'] == dish['title']
    assert response[0]['description'] == dish['description']


def test_update_dish():

    response = client.patch(reverse('update_dish', {
                            'target_menu_id': menu_id, 'target_submenu_id': submenu_id, 'target_dish_id': dish_id}), json=updated_dish)
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == updated_dish['title']
    assert response['description'] == updated_dish['description']


def test_uniq_dish():
    response = client.get(reverse('get_uniq_dish', {'target_menu_id': menu_id,
                          'target_submenu_id': submenu_id, 'target_dish_id': dish_id}))
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == updated_dish['title']
    assert response['description'] == updated_dish['description']
    assert response['price'] == updated_dish['price']


def test_del_dish():
    response = client.delete(reverse('del_dish', {'target_menu_id': menu_id,
                             'target_submenu_id': submenu_id, 'target_dish_id': dish_id}))
    assert response.status_code == 200, 'Fail'
    assert response.json() == {'status': True, 'message': 'The dish has been deleted'}


def test_uniq_dish_1():
    response = client.get(reverse('get_uniq_dish', {'target_menu_id': menu_id,
                          'target_submenu_id': submenu_id, 'target_dish_id': dish_id}))
    assert response.status_code == 404, 'Fail'


def test_get_dishes_1():
    response = client.get(reverse('get_dishes', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_delete_submenu():
    response = client.delete(reverse('delete_submenu', {'target_menu_id': menu_id, 'target_submenu_id': submenu_id}))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The submenu has been deleted'}


def test_get_submenu():
    response = client.get(reverse('get_submenu', {'target_menu_id': menu_id}))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'


def test_delete_menu():
    response = client.delete(reverse('delete_menu', {'target_menu_id': menu_id}))
    assert response.status_code == 200
    assert response.json() == {'status': True, 'message': 'The menu has been deleted'}


def test_get_deleted():
    response = client.get(reverse('get_menu'))
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'
