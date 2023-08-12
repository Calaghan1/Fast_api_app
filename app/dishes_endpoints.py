from fastapi import APIRouter, Depends, BackgroundTasks

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
