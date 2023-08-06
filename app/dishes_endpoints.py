from fastapi import APIRouter, Depends

from repository.dish_repository import DishesRepository
from schemas_all import dish_schemas

dish_router = APIRouter()


@dish_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes')
def get_dishes(target_menu_id: str, target_submenu_id: str, dish: DishesRepository = Depends()) -> list[dish_schemas.ShowDishes]:
    return dish._get_dishes(target_menu_id, target_submenu_id)


@dish_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def get_uniq_dish(target_menu_id, target_submenu_id, target_dish_id, dish: DishesRepository = Depends()) -> dish_schemas.ShowDishes:
    return dish._get_uniq_dish(target_dish_id)


@dish_router.post('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', status_code=201)
def create_dish(target_menu_id, target_submenu_id, dish_data: dish_schemas.Dishescrate, dish: DishesRepository = Depends()) -> dish_schemas.ShowDishes:
    return dish._create_dish(dish_data, target_menu_id, target_submenu_id)


@dish_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def update_dish(target_menu_id, target_submenu_id, target_dish_id, dish_data: dish_schemas.Dishescrate, dish: DishesRepository = Depends()) -> dish_schemas.ShowDishes:

    return dish._update_dish(dish_data, target_menu_id, target_submenu_id, target_dish_id)


@dish_router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}')
def del_dish(target_menu_id, target_submenu_id, target_dish_id, dish: DishesRepository = Depends()) -> dict:

    return dish._delete_dish(target_submenu_id, target_dish_id)
