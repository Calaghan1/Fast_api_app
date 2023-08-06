from fastapi import APIRouter, Depends

import schemas
from crud import MenuRepository

menu_router = APIRouter()


@menu_router.get('/api/v1/menus')
def get_menu(menu: MenuRepository = Depends()) -> list[schemas.ShowMenu]:
    return menu._get_menu()


@menu_router.post('/api/v1/menus', status_code=201)
def create_menu(menu_data: schemas.MenuCreate, menu: MenuRepository = Depends()) -> schemas.ShowMenu:
    return menu._create_menu(menu_data)


@menu_router.get('/api/v1/menus/{target_menu_id}')
def get_uniq_menu(target_menu_id: str, menu: MenuRepository = Depends()) -> schemas.ShowMenu:
    response = menu._get_uniq_menu(target_menu_id)
    print(type(response))
    return response


@menu_router.patch('/api/v1/menus/{target_menu_id}')
def update_menu(menu_data: schemas.MenuCreate, target_menu_id: str, menu: MenuRepository = Depends()) -> schemas.ShowMenu:

    return menu._update_menu(menu_data, target_menu_id)


@menu_router.delete('/api/v1/menus/{target_menu_id}')
def delete_menu(target_menu_id: str, menu: MenuRepository = Depends()) -> dict:

    return menu._delete_menu(target_menu_id)
