from fastapi import BackgroundTasks, Depends

from database.redis_tools import rd
from repository.submenu_repository import SubmenuRepository
from schemas_all import submenu_schemas


class submenus_service:
    def __init__(self, db: SubmenuRepository = Depends()) -> None:
        self.submenu_rep = db

    async def get_submenu(self, menu_id: str) -> list[submenu_schemas.ShowSubmenu]:
        cache = rd.get_value(f'menus-{menu_id}:submenus')
        if cache:
            return cache
        else:
            result = await self.submenu_rep._get_submenu(menu_id)
            rd.set_pair(f'menus-{menu_id}:submenus', result)
            return result

    async def get_uniq_submenu(self, menu_id: str, submenu_id: str) -> submenu_schemas.ShowSubmenu:
        cache = rd.get_value(f'menus-{menu_id}:submenus-{submenu_id}')
        if cache:
            return cache
        else:
            result = await self.submenu_rep._get_uniq_submenu(menu_id, submenu_id)
            rd.set_pair(f'menus-{menu_id}:submenus-{submenu_id}', result)
            return result

    async def create_submenu(self, back_ground_task: BackgroundTasks, menu_id: str, data: submenu_schemas.SubmenuCreate) -> submenu_schemas.ShowSubmenu:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.find_and_del, menu_id)
        back_ground_task.add_task(rd.del_key, 'all_data')
        return await self.submenu_rep._create_submenu(data, menu_id)

    async def update_submenu(self, back_ground_task: BackgroundTasks, menu_id: str, submenu_id: str, data: submenu_schemas.SubmenuCreate) -> submenu_schemas.ShowSubmenu:
        back_ground_task.add_task(rd.find_and_del, submenu_id)
        back_ground_task.add_task(rd.del_key, f'menus-{menu_id}:submenus')
        back_ground_task.add_task(rd.del_key, 'all_data')
        return await self.submenu_rep._update_submenu(data, menu_id, submenu_id)

    async def delete_submenu(self, back_ground_task: BackgroundTasks, menu_id: str, submenu_id: str) -> dict:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.find_and_del, menu_id)
        back_ground_task.add_task(rd.del_key, 'all_data')
        return await self.submenu_rep._delete_submenu(menu_id, submenu_id)
