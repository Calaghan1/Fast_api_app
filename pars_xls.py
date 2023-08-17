import json
import os

import openpyxl

from database.database import SessionLocal
from database.redis_tools import rd
from repository.dish_repository import DishesRepository
from repository.menu_repository import MenuRepository
from repository.submenu_repository import SubmenuRepository
from schemas_all.dish_schemas import Dishescrate
from schemas_all.menu_schemas import MenuCreate
from schemas_all.submenu_schemas import SubmenuCreate

json_path = 'saved_data.json'
path = 'admin/Menu.xlsx'


def check_update(SAVED_DATA: dict) -> bool:
    changes = os.path.getmtime(path)
    if SAVED_DATA['epoch'] != changes:
        SAVED_DATA['epoch'] = changes
        return True
    else:
        return False


def init_saved_data() -> dict:
    with open(json_path) as f:
        data = json.load(f)
    return data


def save_data(data: dict) -> None:
    with open(json_path, 'w') as f:
        json.dump(data, f)


async def task() -> None:
    print('START TASK')
    SAVED_DATA = {}
    NEW_DATA: list = []
    if os.path.exists(json_path):
        NEW_DATA = await get_data()
        SAVED_DATA = init_saved_data()
        if check_update(SAVED_DATA):
            print('update')
            await chek_suh(SAVED_DATA, NEW_DATA)
        else:
            print('no update')
    else:
        print('else')
        SAVED_DATA['epoch'] = os.path.getmtime(path)
        SAVED_DATA['data'] = await get_data()
        SAVED_DATA = await data_to_base(SAVED_DATA)
        save_data(SAVED_DATA)


async def data_to_base(SAVED_DATA: dict) -> dict:
    d: dict = {}
    NEW_SAVED_DATA = {}
    NEW_SAVED_DATA['epoch'] = SAVED_DATA['epoch']
    NEW_SAVED_DATA['data'] = []
    last_menu_id: str = ''
    last_submenu_id: str = ''
    NEW_SAVED_DATA['id_real_id'] = {}
    for data in SAVED_DATA['data']:
        if data['type'] == 'menu':
            d = MenuCreate(title=data['title'], description=data['description'])
            async with SessionLocal() as session:
                menu_rep = MenuRepository(session)
                response = await menu_rep._create_menu(d)
                rd.del_key('menus')
                last_menu_id = str(response.id)
                NEW_SAVED_DATA['id_real_id'][data['id']] = last_menu_id
                NEW_SAVED_DATA['data'].append(data)

        if data['type'] == 'submenu':
            d = SubmenuCreate(title=data['title'], description=data['description'])
            async with SessionLocal() as session:
                submenu_rep = SubmenuRepository(session)
                response = await submenu_rep._create_submenu(d, last_menu_id)
                rd.del_key('menus')
                rd.find_and_del(last_menu_id)
                last_submenu_id = str(response.id)
                NEW_SAVED_DATA['id_real_id'][data['id']] = last_submenu_id
                NEW_SAVED_DATA['data'].append(data)

        if data['type'] == 'dish':
            async with SessionLocal() as session:
                dish_rep = DishesRepository(session)
                d = Dishescrate(title=data['title'], description=data['description'], price=data['price'])
                response = await dish_rep._create_dish(d, last_menu_id, last_submenu_id)
                rd.del_key('menus')
                rd.find_and_del(last_menu_id)
                NEW_SAVED_DATA['id_real_id'][data['id']] = str(response.id)
                NEW_SAVED_DATA['data'].append(data)

    return NEW_SAVED_DATA


async def get_data() -> list:
    last_menu: str = ''
    last_submenu: str = ''
    result = []
    df = openpyxl.load_workbook(path)
    table = df.active
    for row in table.iter_rows(values_only=True):
        d = {}
        if row[0] is not None:
            last_menu = str(float(row[0]))
            d['type'] = 'menu'
            d['id'] = str(float(row[0]))
            d['title'] = row[1]
            d['description'] = row[2]
        elif row[1] is not None:
            last_submenu = last_menu + str(float(row[1]))
            d['type'] = 'submenu'
            d['id'] = last_menu + str(float(row[1]))
            d['title'] = row[2]
            d['description'] = row[3]
            d['menu_id'] = last_menu
        elif row[2] is not None:
            d['type'] = 'dish'
            d['id'] = last_menu + last_submenu + str(float(row[2]))
            d['title'] = row[3]
            d['description'] = row[4]
            d['price'] = row[5]
            d['submenu_id'] = last_submenu
            d['menu_id'] = last_menu
        if d != {}:
            result.append(d)
    return result


async def create_in_db(create: list, SAVED_DATA: dict) -> dict:
    d: dict = {}
    for data in create:
        if data['type'] == 'menu':
            async with SessionLocal() as session:
                menu_rep = MenuRepository(session)
                d = MenuCreate(title=data['title'], description=data['description'])
                response = await menu_rep._create_menu(d)
                rd.del_key('menus')
                SAVED_DATA['data'].append(data)
                SAVED_DATA['id_real_id'][data['id']] = str(response.id)

        if data['type'] == 'submenu':
            async with SessionLocal() as session:
                submenu_rep = SubmenuRepository(session)
                menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
                d = SubmenuCreate(title=data['title'], description=data['description'])
                response = await submenu_rep._create_submenu(d, menu_id)
                rd.del_key('menus')
                rd.find_and_del(menu_id)
                SAVED_DATA['data'].append(data)
                SAVED_DATA['id_real_id'][data['id']] = str(response.id)

        if data['type'] == 'dish':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['submenu_id']))
            async with SessionLocal() as session:
                dish_rep = DishesRepository(session)
                menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
                d = Dishescrate(title=data['title'], description=data['description'], price=data['price'])
                response = await dish_rep._create_dish(d, menu_id, submenu_id)
                rd.del_key('menus')
                rd.find_and_del(menu_id)
                SAVED_DATA['data'].append(data)
                SAVED_DATA['id_real_id'][data['id']] = str(response.id)
    return SAVED_DATA


async def update_in_db(update: list, SAVED_DATA: dict) -> dict:
    d: dict = {}
    for data in update:
        if data['type'] == 'menu':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            async with SessionLocal() as session:
                menu_rep = MenuRepository(session)
                d = MenuCreate(title=data['title'], description=data['description'])
                response = await menu_rep._update_menu(d, menu_id)
                rd.del_key('menus')
                rd.del_key(f'menus-{menu_id}')
                SAVED_DATA['data'].append(data)
                SAVED_DATA['id_real_id'][data['id']] = str(response.id)

        if data['type'] == 'submenu':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            async with SessionLocal() as session:
                submenu_rep = SubmenuRepository(session)
                d = SubmenuCreate(title=data['title'], description=data['description'])
                response = await submenu_rep._update_submenu(d, menu_id, submenu_id)
                rd.find_and_del(submenu_id)
                rd.del_key(f'menus-{menu_id}:submenus')
                SAVED_DATA['data'].append(data)
                SAVED_DATA['id_real_id'][data['id']] = str(response.id)

        if data['type'] == 'dish':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['submenu_id']))
            dish_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            async with SessionLocal() as session:
                dish_rep = DishesRepository(session)
                d = Dishescrate(title=data['title'], description=data['description'], price=data['price'])
                response = await dish_rep._update_dish(d, menu_id, submenu_id, dish_id)
                rd.del_key(f'menus-{menu_id}:submenu-{submenu_id}:dishes')
                rd.find_and_del(dish_id)
                SAVED_DATA['data'].append(data)
                SAVED_DATA['id_real_id'][data['id']] = str(response.id)

        SAVED_DATA['data'] = update_in_saved_data(data, SAVED_DATA['data'])
    return SAVED_DATA


async def del_in_db(delete: list, SAVED_DATA: dict) -> dict:
    deleted_menu = []
    deleted_submenu = []
    for data in delete:
        print(data)
        if data['type'] == 'menu':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            async with SessionLocal() as session:
                menu_rep = MenuRepository(session)

                await menu_rep._delete_menu(menu_id)
                rd.del_key('menus')
                rd.find_and_del(menu_id)
                deleted_menu.append(menu_id)

        if data['type'] == 'submenu':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            if menu_id not in deleted_menu:
                async with SessionLocal() as session:
                    submenu_rep = SubmenuRepository(session)

                    await submenu_rep._delete_submenu(menu_id, submenu_id)
                    rd.del_key('menus')
                    rd.find_and_del(menu_id)
                    deleted_submenu.append(submenu_id)

        if data['type'] == 'dish':
            menu_id = SAVED_DATA['id_real_id'].get(str(data['menu_id']))
            submenu_id = SAVED_DATA['id_real_id'].get(str(data['submenu_id']))
            dish_id = SAVED_DATA['id_real_id'].get(str(data['id']))
            if menu_id not in deleted_menu and submenu_id not in deleted_submenu:
                async with SessionLocal() as session:
                    dish_rep = DishesRepository(session)
                    await dish_rep._delete_dish(submenu_id, dish_id)
                    rd.del_key('menus')
                    rd.find_and_del(menu_id)

        SAVED_DATA['data'] = delete_in_saved_data(data, SAVED_DATA['data'])
    return SAVED_DATA


def update_in_saved_data(data_up: dict, SAVED_DATA: dict) -> dict:
    for i in range(len(SAVED_DATA)):
        if SAVED_DATA[i]['id'] == data_up['id']:
            SAVED_DATA[i] = data_up
    return SAVED_DATA


def delete_in_saved_data(data_del: dict, SAVED_DATA: list) -> list:
    ia = 0
    for i in range(len(SAVED_DATA)):
        if SAVED_DATA[i]['id'] == data_del['id']:
            ia = i
    SAVED_DATA.remove(SAVED_DATA[ia])
    return SAVED_DATA


async def chek_suh(SAVED_DATA: dict, NEW_DATA: list):
    new_id = [s['id'] for s in NEW_DATA]
    old_id = [s['id'] for s in SAVED_DATA['data']]
    print(new_id)
    print(old_id)
    delete = [data for data in SAVED_DATA['data'] if data['id'] not in new_id]
    create = [data for data in NEW_DATA if data['id'] not in old_id]
    update = []
    for data in NEW_DATA:
        for data_s in SAVED_DATA['data']:
            if data['id'] == data_s['id'] and data != data_s:
                update.append(data)

    if create:
        SAVED_DATA = await create_in_db(create, SAVED_DATA)
    if update:
        SAVED_DATA = await update_in_db(update, SAVED_DATA)
    if delete:

        SAVED_DATA = await del_in_db(delete, SAVED_DATA)

    save_data(SAVED_DATA)
