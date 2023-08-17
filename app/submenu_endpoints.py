from fastapi import APIRouter, BackgroundTasks, Depends

from schemas_all import submenu_schemas
from services.submenu_service import submenus_service

submenu_router = APIRouter()


@submenu_router.get('/api/v1/menus/{target_menu_id}/submenus')
async def get_submenu(target_menu_id, submenu: submenus_service = Depends()):
    return await submenu.get_submenu(target_menu_id)


@submenu_router.get('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def get_uniq_submenu(target_menu_id, target_submenu_id, submenu: submenus_service = Depends()):
    return await submenu.get_uniq_submenu(target_menu_id, target_submenu_id)


@submenu_router.post('/api/v1/menus/{target_menu_id}/submenus', response_model=submenu_schemas.ShowSubmenu, status_code=201)
async def create_submenu(target_menu_id, submenu_data: submenu_schemas.SubmenuCreate, back_ground_task: BackgroundTasks, submenu: submenus_service = Depends()):
    return await submenu.create_submenu(back_ground_task, target_menu_id, submenu_data)


@submenu_router.patch('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def update_submenu(target_menu_id, target_submenu_id, submenu_data: submenu_schemas.SubmenuCreate, back_ground_task: BackgroundTasks, submenu: submenus_service = Depends()):
    return await submenu.update_submenu(back_ground_task, target_menu_id, target_submenu_id, submenu_data)


@submenu_router.delete('/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}')
async def delete_submenu(target_menu_id, target_submenu_id, back_ground_task: BackgroundTasks, submenu: submenus_service = Depends()):
    return await submenu.delete_submenu(back_ground_task, target_menu_id, target_submenu_id)
