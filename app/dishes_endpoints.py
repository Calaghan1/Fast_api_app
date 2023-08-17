from fastapi import APIRouter, BackgroundTasks, Depends

from schemas_all import dish_schemas
from services.dishes_service import dishes_service

dish_router = APIRouter()


@dish_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def get_dishes(target_menu_id: str, target_submenu_id: str, dish: dishes_service = Depends()) -> list[dish_schemas.ShowDishes]:
    return await dish.get_dishes(target_menu_id, target_submenu_id, )


@dish_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def get_uniq_dish(target_menu_id, target_submenu_id, target_dish_id, dish: dishes_service = Depends()) -> dish_schemas.ShowDishes:
    return await dish.get_uniq_dish(target_menu_id, target_submenu_id, target_dish_id)


@dish_router.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=201)
async def create_dish(target_menu_id, target_submenu_id, dish_data: dish_schemas.Dishescrate, back_ground_task: BackgroundTasks, dish: dishes_service = Depends()) -> dish_schemas.ShowDishes:
    return await dish.create_dish(back_ground_task, target_menu_id, target_submenu_id, dish_data)


@dish_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def update_dish(target_menu_id, target_submenu_id, target_dish_id, dish_data: dish_schemas.Dishescrate, back_ground_task: BackgroundTasks, dish: dishes_service = Depends()) -> dish_schemas.ShowDishes:
    return await dish.update_dish(back_ground_task, target_menu_id, target_submenu_id, target_dish_id, dish_data)


@dish_router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
async def del_dish(target_menu_id, target_submenu_id, target_dish_id, back_ground_task: BackgroundTasks, dish: dishes_service = Depends()) -> dict:
    return await dish.delete_dish(back_ground_task, target_menu_id, target_submenu_id, target_dish_id)

    # if data['type'] == 'menu':
    #     d['title'] = data['title']
    #     d['description'] = data['description']
    #     print(d)
    #     response = requests.post('http://127.0.0.1:8000/api/v1/menus', json = d)
    #     data['real_id'] = last_menu_id = response.json()['id']
    #     NEW_SAVED_DATA.append(data)

    # if data['type'] == 'submenu':
    #     d['title'] = data['title']
    #     d['description'] = data['description']
    #     response = requests.post(f'http://127.0.0.1:8000/api/v1/menus/{last_menu_id}/submenus', json = d)
    #     data['real_id'] = last_submenu_id = response.json()['id']
    #     NEW_SAVED_DATA.append(data)

    # if data['type'] == 'dish':
    #     d['title'] = data['title']
    #     d['description'] = data['description']
    #     d['price'] = data['price']
    #     response = requests.post(f'http://127.0.0.1:8000/api/v1/menus/{last_menu_id}/submenus/{last_submenu_id}/dishes', json = d)
    #     data['real_id'] = response.json()['id']
    #     NEW_SAVED_DATA.append(data)
