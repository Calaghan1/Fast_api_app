from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
import httpx
import models
client = TestClient(app)

menu = {'title': 'menu 1', 'description': 'desc 1'}
submenu = {'title': 'submenu 1', 'description': 'sub desc 1'}
updated_submenu = {'title': 'updated submenu 1',  'description': ' updated sub desc 1'}
menu_id = ''
submenu_id = ' '
# def test_drop_tables():
#     models.Menu.__table__.drop()


def test_create_test_menu():
    global menu_id
    response = client.post("/api/v1/menus", json=menu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == menu['title']
    assert response['description'] == menu['description']
    menu_id = str(response['id'])
    print(menu_id)

def test_get_submenu():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'

def test_create_submenu():
    global submenu_id
    response = client.post(f"/api/v1/menus/{menu_id}/submenus", json=submenu)
    assert response.status_code == 201
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']
    submenu_id = str(response['id'])

def test_get_submenu_1():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response[0]['title'] == submenu['title']
    assert response[0]['description'] == submenu['description']


def test_get_uniq_submenu():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == submenu['title']
    assert response['description'] == submenu['description']


def test_update_submenu():
    response = client.patch(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}", json=updated_submenu)
    assert response.status_code == 200
    response = response.json()
    assert response['title'] == updated_submenu['title']
    assert response['description'] == updated_submenu['description']
    
def test_get_uniq_submenu_1():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200, 'Fail'
    response = response.json()
    assert response['title'] == updated_submenu['title']
    assert response['description'] == updated_submenu['description']
    
def test_delete_submenu():
    response = client.delete(f"/api/v1/menus/{menu_id}/submenus/{submenu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message":"The menu has been deleted"}


def test_get_submenu_1_1():
    response = client.get(f"/api/v1/menus/{menu_id}/submenus")
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'
    
def test_delete_menu_1():
    response = client.delete(f"/api/v1/menus/{menu_id}")
    assert response.status_code == 200
    assert response.json() == {"status": True, "message":"The menu has been deleted"}    

def test_get_deleted():
    response = client.get('/api/v1/menus')
    assert response.status_code == 200, 'Fail'
    assert response.json() == [], 'Fail'

