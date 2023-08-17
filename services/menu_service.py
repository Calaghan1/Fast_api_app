from fastapi import BackgroundTasks, Depends

from database.redis_tools import rd
from repository.menu_repository import MenuRepository
from schemas_all import menu_schemas


class menu_service:
    def __init__(self, db: MenuRepository = Depends()) -> None:
        self.menu_rep = db

    async def get_menu(self) -> list[menu_schemas.ShowMenu]:
        cache = rd.get_value('menus')
        if cache:
            print('cache')
            return cache
        else:
            result = await self.menu_rep._get_menu()
            rd.set_pair('menus', result)
            return result

    async def get_uniq_menu(self, menu_id: str) -> menu_schemas.ShowMenu:
        cache = rd.get_value(f'menus-{menu_id}')
        if cache:
            return cache
        else:
            result = await self.menu_rep._get_uniq_menu(menu_id)
            rd.set_pair(f'menus-{menu_id}', result)
            return result

    async def create_menu(self, back_ground_task: BackgroundTasks, data: menu_schemas.MenuCreate) -> menu_schemas.ShowMenu:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.del_key, 'all_data')
        return await self.menu_rep._create_menu(data)

    async def update_menu(self, back_ground_task: BackgroundTasks, menu_id: str, data: menu_schemas.MenuCreate) -> menu_schemas.ShowMenu:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.del_key, f'menus-{menu_id}')
        back_ground_task.add_task(rd.del_key, 'all_data')
        return await self.menu_rep._update_menu(data, menu_id)

    async def delete_menu(self, back_ground_task: BackgroundTasks, menu_id: str) -> dict:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.find_and_del, menu_id)
        back_ground_task.add_task(rd.del_key, 'all_data')
        return await self.menu_rep._delete_menu(menu_id)

    async def get_all(self) -> list:
        respose = await self.menu_rep._get_all_data()
        rd.set_pair('all_data', respose)
        return respose
