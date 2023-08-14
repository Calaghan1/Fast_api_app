import pandas as pd
import csv
import os
from schemas_all.dish_schemas import Dishescrate
from schemas_all.menu_schemas import MenuCreate
from schemas_all.submenu_schemas import SubmenuCreate
from repository.menu_repository import MenuRepository
import asyncio
from fastapi.testclient import TestClient
from app.main import app, reverse
import openpyxl
import json
import requests
from itertools import zip_longest
SAVED_DATA = {}
json_path = 'saved_data.json'
path = 'admin/Menu.xlsx'


def check_update(path: str) -> bool:
    changes = os.path.getmtime(path)
    if SAVED_DATA['epoch'] != changes:
        SAVED_DATA['epoch'] = changes
        return True
    else:
        return False


def init_saved_data():
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data

def save_data(data):
        with open(json_path, 'w') as f:
            data = json.dump(data, f)

        
        
async def task():
    global SAVED_DATA
    if os.path.exists(json_path):
        print("if")
        SAVED_DATA = init_saved_data()
        # if check_update(path):
        #     pass
        await check_updates_in_file(SAVED_DATA)
    else:
        print("else")
        SAVED_DATA['epoch'] = os.path.getmtime(path)
        SAVED_DATA['data'] = await get_data()
        # print(SAVED_DATA['data'])
        #добавить в базу
        # SAVED_DATA = await data_to_base(SAVED_DATA)
        save_data(SAVED_DATA)
    
async def data_to_base(SAVED_DATA):
    d = {}
    NEW_SAVED_DATA = []
    last_menu_id = None
    last_submenu_id = None
    for data in SAVED_DATA['data']:
        print(data)
        d['title'] = data['title']
        d['description'] = data['description']
        response = requests.post('http://127.0.0.1:8000/api/v1/menus', json = d)
        data['real_id'] = response.json()['id']
        for submenus in data['submenus']:
            d = {}
            d['title'] = submenus['title']
            d['description'] = submenus['description']
            menu_id  = data['real_id']
            response = requests.post(f'http://127.0.0.1:8000/api/v1/menus/{menu_id}/submenus', json = d)
            submenus['real_id'] = response.json()['id']
            for dish in submenus['dishes']:
                d = {}
                d['title'] = dish['title']
                d['description'] = dish['description']
                d['price'] = dish['price']
                submenu_id = submenus['real_id']
                response = requests.post(f'http://127.0.0.1:8000/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes', json = d)
                dish['real_id'] = response.json()['id']
        NEW_SAVED_DATA.append(data)
            
    return NEW_SAVED_DATA
            
        
async def get_data():
    last_menu = 0
    last_submenu = 0
    result = []
    d_menu = {}
    d_submenu = {}
    d_dish = {}
    df = openpyxl.load_workbook(path)
    table = df.active
    i = -1
    for row in table.iter_rows(values_only=True):
        if row[0] is not None:
            if d_menu != {}:
                result.append(d_menu)
            i = -1
            d_menu = {}
            last_menu = row[0]
            d_menu['type'] = 'menu'
            d_menu['id'] = row[0]
            d_menu['title'] = row[1]
            d_menu['description'] = row[2]
            d_menu['submenus'] = []
        elif row[1] is not None:
            i += 1
            d_submenu = {}
            last_submenu = row[1]
            d_submenu['type'] = 'submenu'
            d_submenu['id'] = row[1]
            d_submenu['title'] = row[2]
            d_submenu['description'] = row[3]
            d_submenu['menu_id'] = last_menu
            d_submenu['dishes'] = []
            d_menu['submenus'].append(d_submenu)
        elif row[2] is not None:
            d_dish = {}
            d_dish['type'] = 'dish'
            d_dish['id'] = row[2]
            d_dish['title'] = row[3]
            d_dish['description'] = row[4]
            d_dish['price'] = row[5]
            d_dish['submenu_id'] = last_submenu
            d_menu['submenus'][i]['dishes'].append(d_dish)
            # d_submenu['dishes'].append(d_dish)
    
    result.append(d_menu)
 
    return result

def maxx(one, two):
    if len(one) < len(two):
        return len(one)
    return len(two)

async def check_updates_in_file(SAVED_DATA):
    NEW_DATA = await get_data()
    # for new_data, saved_data in zip_longest(NEW_DATA, SAVED_DATA):
    #     print(new_data['title'])
    #     print(saved_data['title'])
    #     for new_submenu, saved_submenu in zip_longest(new_data['submenus'], saved_data['submenus']):
    #         print(new_submenu['title'])
    #         print(saved_submenu['title'])
    #         for new_dishes, saved_dishes in zip_longest(new_submenu['dishes'], saved_submenu['dishes']):
    #             print(new_dishes['title'])
    #             print(saved_dishes['title'])
    
    for key in NEW_DATA:
        # if key in SAVED_DATA and SAVED_DATA[key] != NEW_DATA[key]:
        #     print(SAVED_DATA[key])
        #     print(NEW_DATA[key])
        print(NEW_DATA[key])
    
    



asyncio.run(task())