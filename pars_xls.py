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

# # test_l_1 = [1, 2 ,3]
# # test_l_2 = [1, 2, 4]
# # print(test_l_1 == test_l_2)
# menu_rep = MenuRepository()
# change = os.path.getmtime('admin/t.txt')
# print(change)

# async def read_xlsx_data(path: str):
#     df = openpyxl.load_workbook(path)
#     table = df.active
#     for row in table.iter_rows(value_only=True):
#         if row[0] is not None:
#             pass
SAVED_DATA = {}

def check_update(path: str) -> bool:
    changes = os.path.getmtime(path)
    if SAVED_DATA['epoch'] != changes:
        SAVED_DATA['epoch'] = changes
        return True
    else:
        return False


    
async def task():
    path = 'admin/Menu.xlsx'
    if 'epoch' not in SAVED_DATA:
        SAVED_DATA['epoch'] = os.path.getmtime(path)
        SAVED_DATA['data'] = await get_data(path)
    if check_update(path):
        new_data = await get_data(path)
        print(new_data)
    
    
async def get_data(path: str):
    last_menu = 0
    last_submenu = 0
    result = []
    df = openpyxl.load_workbook(path)
    table = df.active
    for row in table.iter_rows(values_only=True):
        d = {}
        if row[0] is not None:
            last_menu = row[0]
            d['type'] = 'menu'
            d['id'] = row[0]
            d['title'] = row[1]
            d['description'] = row[2]
        elif row[1] is not None:
            last_submenu = row[1]
            d['type'] = 'submenu'
            d['id'] = row[1]
            d['title'] = row[2]
            d['description'] = row[3]
            d['menu_id'] = last_menu
        elif row[2] is not None:
            d['type'] = 'dish'
            d['id'] = row[2]
            d['title'] = row[3]
            d['description'] = row[4]
            d['price'] = row[5]
            d['submenu_id'] = last_submenu
        result.append(d)
    return result


asyncio.run(task())