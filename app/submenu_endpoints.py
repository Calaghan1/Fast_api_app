from fastapi import APIRouter, Depends

from schemas_all import submenu_schemas
from services.submenu_service import submenus_service

submenu_router = APIRouter()


@submenu_router.get('/api/v1/menus/{target_menu_id}/submenus')
def get_submenu(target_menu_id, submenu: submenus_service = Depends()):
    return submenu.get_submenu(target_menu_id)


@submenu_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def get_uniq_submenu(target_menu_id, target_submenu_id, submenu: submenus_service = Depends()):
    return submenu.get_uniq_submenu(target_menu_id, target_submenu_id)


@submenu_router.post('/api/v1/menus/{target_menu_id}/submenus', response_model=submenu_schemas.ShowSubmenu, status_code=201)
def create_submenu(target_menu_id, submenu_data: submenu_schemas.SubmenuCreate, submenu: submenus_service = Depends()):
    return submenu.create_submenu(target_menu_id, submenu_data)


@submenu_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def update_submenu(target_menu_id, target_submenu_id, submenu_data: submenu_schemas.SubmenuCreate, submenu: submenus_service = Depends()):
    return submenu.update_submenu(target_menu_id, target_submenu_id, submenu_data)


@submenu_router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenu(target_menu_id, target_submenu_id, submenu: submenus_service = Depends()):
    return submenu.delete_submenu(target_menu_id, target_submenu_id)
