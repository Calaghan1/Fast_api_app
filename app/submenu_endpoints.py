from fastapi import APIRouter, Depends

import schemas
from crud import SubmenuRepository

submenu_router = APIRouter()


@submenu_router.get('/api/v1/menus/{target_menu_id}/submenus')
def get_submenu(target_menu_id, submenu: SubmenuRepository = Depends()):
    return submenu._get_submenu(target_menu_id)


@submenu_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def get_uniq_submenu(target_menu_id, target_submenu_id, submenu: SubmenuRepository = Depends()):
    return submenu._get_uniq_submenu(target_submenu_id)


@submenu_router.post('/api/v1/menus/{target_menu_id}/submenus', response_model=schemas.ShowSubmenu, status_code=201)
def create_submenu(target_menu_id, submenu_data: schemas.SubmenuCreate, submenu: SubmenuRepository = Depends()):
    return submenu._create_submenu(submenu_data, target_menu_id)


@submenu_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def update_submenu(target_menu_id, target_submenu_id, submenu_data: schemas.SubmenuCreate, submenu: SubmenuRepository = Depends()):
    return submenu._update_submenu(submenu_data, target_submenu_id)


@submenu_router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
def delete_submenu(target_menu_id, target_submenu_id, submenu: SubmenuRepository = Depends()):
    return submenu._delete_submenu(target_menu_id, target_submenu_id)
