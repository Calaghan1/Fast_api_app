import os
import asyncio
import openpyxl
import json
from app.main import app, reverse
from fastapi.testclient import TestClient

json_path = 'saved_data.json'
path = 'admin/Menu.xlsx'

client = TestClient(app)
def check_update(SAVED_DATA: dict) -> bool:
    changes = os.path.getmtime(path)
    if SAVED_DATA['epoch'] != changes:
        SAVED_DATA['epoch'] = changes
        return True
    else:
        return False


def init_saved_data() -> dict:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data

def save_data(data : dict) -> None:
        with open(json_path, 'w') as f:
            data = json.dump(data, f)

        
        
async def task() -> None:
    print("START TASK")
    SAVED_DATA = {}
    NEW_DATA = {}
    if os.path.exists(json_path):
        NEW_DATA = await get_data()
        SAVED_DATA = init_saved_data()
        if check_update(SAVED_DATA):
            print('update')
            await chek_suh(SAVED_DATA, NEW_DATA)
        else:
            print("no update")
    else:
        print("else")
        SAVED_DATA['epoch'] = os.path.getmtime(path)
        SAVED_DATA['data'] = await get_data()
        SAVED_DATA= await data_to_base(SAVED_DATA)
        save_data(SAVED_DATA)
    
async def data_to_base(SAVED_DATA: dict) -> dict:
    d = {}
    NEW_SAVED_DATA = {}
    NEW_SAVED_DATA['epoch'] = SAVED_DATA['epoch']
    NEW_SAVED_DATA['data'] = []
    last_menu_id = None
    last_submenu_id = None
    NEW_SAVED_DATA['id_real_id'] = {}
    for data in SAVED_DATA['data']:
        if data['type'] == 'menu':
            d['title'] = data['title']
            d['description'] = data['description']
            response = client.post('http://0.0.0.0:8000/api/v1/menus', json = d)
            last_menu_id = response.json()['id']
            NEW_SAVED_DATA['id_real_id'][data['id']] = last_menu_id
            NEW_SAVED_DATA['data'].append(data)
            
        if data['type'] == 'submenu':
            d['title'] = data['title']
            d['description'] = data['description']
            response = client.post(f'http://0.0.0.0:8000/api/v1/menus/{last_menu_id}/submenus', json = d)
            last_submenu_id = response.json()['id']
            NEW_SAVED_DATA['id_real_id'][data['id']] = last_submenu_id
            NEW_SAVED_DATA['data'].append(data)
            
        if data['type'] == 'dish':
            d['title'] = data['title']
            d['description'] = data['description']
            d['price'] = data['price']
            response = client.post(f'http://0.0.0.0:8000/api/v1/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes', json = d)
            NEW_SAVED_DATA['id_real_id'][data['id']] = response.json()['id']
            NEW_SAVED_DATA['data'].append(data)
            
    return NEW_SAVED_DATA
            
        
async def get_data() -> list:
    last_menu = 0
    last_submenu = 0
    result = []
    df = openpyxl.load_workbook(path)
    table = df.active
    for row in table.iter_rows(values_only=True):
        d = {}
        if row[0] is not None:
            last_menu = str(row[0])
            d['type'] = 'menu'
            d['id'] = str(row[0])
            d['title'] = row[1]
            d['description'] = row[2]
        elif row[1] is not None:
            last_submenu = str(last_menu) + str(row[1])
            d['type'] = 'submenu'
            d['id'] = str(last_menu) + str(row[1])
            d['title'] = row[2]
            d['description'] = row[3]
            d['menu_id'] = last_menu
        elif row[2] is not None:
            d['type'] = 'dish'
            d['id'] = str(last_menu) + str(last_submenu) + str(row[2])
            d['title'] = row[3]
            d['description'] = row[4]
            d['price'] = row[5]
            d['submenu_id'] = last_submenu
            d['menu_id'] = last_menu
        if d != {}:
            result.append(d)
    return result

def create_in_db(create : list, SAVED_DATA: dict) -> dict:
    d = {}
    for data in create:
        if data['type'] == 'menu':
            d['title'] = data['title']
            d['description'] = data['description']
            response = client.post('http://0.0.0.0:8000/api/v1/menus', json = d)
            SAVED_DATA['data'].append(data)
            SAVED_DATA['id_real_id'][data['id']] = response.json()['id']
            
        if data['type'] == 'submenu':
            d['title'] = data['title']
            d['description'] = data['description']
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            response = client.post(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}/submenus', json = d)
            SAVED_DATA['id_real_id'][data['id']] = response.json()[id]
        if data['type'] == 'dish':
            d['title'] = data['title']
            d['description'] = data['description']
            d['price'] = data['price']
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['submenu_id']))
            response = client.post(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json = d)
            SAVED_DATA['data'].append(data)
            SAVED_DATA['id_real_id'][data['id']] = response.json()['id']
    return SAVED_DATA
            
def update_in_db(update: list, SAVED_DATA: dict) -> dict:
    d = {}
    for data in update:
        if data['type'] == 'menu':
            d['title'] = data['title']
            d['description'] = data['description']
            menu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            response = client.patch(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}', json = d)
            
        if data['type'] == 'submenu':
            d['title'] = data['title']
            d['description'] = data['description']
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            response = client.patch(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}', json = d)
            
        if data['type'] == 'dish':
            d['title'] = data['title']
            d['description'] = data['description']
            d['price'] = data['price']
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['submenu_id']))
            dish_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            response = client.patch(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}', json = d)
                 
        SAVED_DATA['data'] = update_in_saved_data(data, SAVED_DATA['data'])
    return SAVED_DATA

def del_in_db(delete: list, SAVED_DATA: dict) -> dict:
    for data in delete:
        print(data)
        if data['type'] == 'menu':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            response = client.delete(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}')
            
        if data['type'] == 'submenu':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            response = client.delete(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}')
            
        if data['type'] == 'dish':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['submenu_id']))
            dish_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            response = client.delete(f'http://0.0.0.0:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}')
                 
        SAVED_DATA['data'] = delete_in_saved_data(data, SAVED_DATA['data'])
    return SAVED_DATA
        
def update_in_saved_data(data_up: dict, SAVED_DATA: dict) -> dict:
    for i in range(len(SAVED_DATA)):
        if SAVED_DATA[i]['id'] == data_up['id']:
            SAVED_DATA[i] = data_up
    return SAVED_DATA


def delete_in_saved_data(data_del: dict, SAVED_DATA: dict) -> dict:
    ia = 0
    for i in range(len(SAVED_DATA)):
        if SAVED_DATA[i]['id'] == data_del['id']:
            ia = i
    SAVED_DATA.remove(SAVED_DATA[ia])
    return SAVED_DATA



async def chek_suh(SAVED_DATA: dict, NEW_DATA: dict):
    new_id = [s['id'] for s in NEW_DATA]
    old_id = [s['id'] for s in SAVED_DATA['data']]
    
    delete = [data for data in SAVED_DATA['data'] if data['id'] not in new_id]
    create = [data for data in NEW_DATA if data['id'] not in old_id]
    update = []
    for data in NEW_DATA:
        for data_s in SAVED_DATA['data']:
            if data['id'] == data_s['id'] and data != data_s:
                update.append(data)
    print(delete)
    for d in delete:
        print(SAVED_DATA['id_real_id'].get(d['id']))
    print(create)
    print(update)
    if create:
        SAVED_DATA = create_in_db(create, SAVED_DATA)
    if update:
        SAVED_DATA = update_in_db(update, SAVED_DATA)
    if delete:
        print(delete)
        SAVED_DATA = del_in_db(delete, SAVED_DATA)  
    save_data(SAVED_DATA)
    
