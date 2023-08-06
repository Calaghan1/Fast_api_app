from fastapi import APIRouter, Depends

import schemas
from crud import DishesRepository

dish_router = APIRouter()


@dish_router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def get_dishes(api_test_menu_id: str, api_test_submenu_id: str, dish: DishesRepository = Depends()):
    return dish._get_dishes(api_test_menu_id, api_test_submenu_id)


@dish_router.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def get_uniq_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, dish: DishesRepository = Depends()):
    return dish._get_uniq_dish(api_test_dish_id)


@dish_router.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', status_code=201)
def create_dish(api_test_menu_id, api_test_submenu_id, dish_data: schemas.Dishescrate, dish: DishesRepository = Depends()):
    return dish._create_dish(dish_data, api_test_menu_id, api_test_submenu_id)


@dish_router.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def update_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, dish_data: schemas.Dishescrate, dish: DishesRepository = Depends()):

    return dish._update_dish(dish_data, api_test_menu_id, api_test_submenu_id, api_test_dish_id)


@dish_router.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def del_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, dish: DishesRepository = Depends()):

    return dish._delete_dish(api_test_submenu_id, api_test_dish_id)
