from fastapi import APIRouter, Depends

from schemas_all import menu_schemas
from services.menu_service import menu_service

menu_router = APIRouter()


@menu_router.get('/api/v1/menus')
async def get_menu(menu: menu_service = Depends()) -> list[menu_schemas.ShowMenu]:
    return await menu.get_menu()


@menu_router.post('/api/v1/menus', status_code=201)
async def create_menu(menu_data: menu_schemas.MenuCreate, menu: menu_service = Depends()) -> menu_schemas.ShowMenu:
    return await menu.create_menu(menu_data)


@menu_router.get('/api/v1/menus/{target_menu_id}')
async def get_uniq_menu(target_menu_id: str, menu: menu_service = Depends()) -> menu_schemas.ShowMenu:
    return await menu.get_uniq_menu(target_menu_id)


@menu_router.patch('/api/v1/menus/{target_menu_id}')
async def update_menu(menu_data: menu_schemas.MenuCreate, target_menu_id: str, menu: menu_service = Depends()) -> menu_schemas.ShowMenu:
    return await menu.update_menu(target_menu_id, menu_data)


@menu_router.delete('/api/v1/menus/{target_menu_id}')
async def delete_menu(target_menu_id: str, menu: menu_service = Depends()) -> dict:

    return await menu.delete_menu(target_menu_id)
