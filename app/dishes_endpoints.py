from fastapi import APIRouter, Depends

from schemas_all import dish_schemas
from services.dishes_service import dishes_service

dish_router = APIRouter()


@dish_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
def get_dishes(target_menu_id: str, target_submenu_id: str, dish: dishes_service = Depends()) -> list[dish_schemas.ShowDishes]:
    return dish.get_dishes(target_menu_id, target_submenu_id, )


@dish_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def get_uniq_dish(target_menu_id, target_submenu_id, target_dish_id, dish: dishes_service = Depends()) -> dish_schemas.ShowDishes:
    return dish.get_uniq_dish(target_menu_id, target_submenu_id, target_dish_id)


@dish_router.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=201)
def create_dish(target_menu_id, target_submenu_id, dish_data: dish_schemas.Dishescrate, dish: dishes_service = Depends()) -> dish_schemas.ShowDishes:
    return dish.create_dish(target_menu_id, target_submenu_id, dish_data)


@dish_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def update_dish(target_menu_id, target_submenu_id, target_dish_id, dish_data: dish_schemas.Dishescrate, dish: dishes_service = Depends()) -> dish_schemas.ShowDishes:

    return dish.update_dish(target_menu_id, target_submenu_id, target_dish_id, dish_data)


@dish_router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def del_dish(target_menu_id, target_submenu_id, target_dish_id, dish: dishes_service = Depends()) -> dict:

    return dish.delete_dish(target_menu_id, target_submenu_id, target_dish_id)
