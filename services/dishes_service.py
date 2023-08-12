from fastapi import Depends, BackgroundTasks

from database.redis_tools import rd
from repository.dish_repository import DishesRepository
from schemas_all import dish_schemas


class dishes_service:
    def __init__(self, db: DishesRepository = Depends()) -> None:
        self.dish_rep = db

    async def get_dishes(self, menu_id: str, submenu_id: str) -> list[dish_schemas.ShowDishes]:
        cache = rd.get_value(f'menus-{menu_id}:submenu-{submenu_id}:dishes')
        if cache:
            return cache
        else:
            result = await self.dish_rep._get_dishes(menu_id, submenu_id)
            rd.set_pair(f'menus-{menu_id}:submenu-{submenu_id}:dishse', result)
            return result

    async def get_uniq_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> dish_schemas.ShowDishes:
        cache = rd.get_value(f'menus-{menu_id}:submenu-{submenu_id}:dishes-{dish_id}')
        if cache:
            return cache
        else:
            result = await self.dish_rep._get_uniq_dish(dish_id)
            rd.set_pair(f'menus-{menu_id}:submenu-{submenu_id}:dishes-{dish_id}', result)
            return result

    async def update_dish(self, back_ground_task: BackgroundTasks, menu_id: str, submenu_id: str, dish_id: str, data: dish_schemas.Dishescrate) -> dish_schemas.ShowDishes:
        back_ground_task.add_task(rd.del_key, f'menus-{menu_id}:submenu-{submenu_id}:dishes')
        back_ground_task.add_task(rd.find_and_del, dish_id)
        # rd.del_key(f'menus-{menu_id}:submenu-{submenu_id}:dishes')
        # rd.find_and_del(dish_id)
        return await self.dish_rep._update_dish(data, menu_id, submenu_id, dish_id)

    async def create_dish(self, back_ground_task: BackgroundTasks, menu_id: str, submenu_id: str, data: dish_schemas.Dishescrate) -> dish_schemas.ShowDishes:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.find_and_del, menu_id)
        # rd.del_key('menus')
        # rd.find_and_del(menu_id)
        return await self.dish_rep._create_dish(data, menu_id, submenu_id)

    async def delete_dish(self, back_ground_task: BackgroundTasks, menu_id: str, submenu_id: str, dish_id: str) -> dict:
        back_ground_task.add_task(rd.del_key, 'menus')
        back_ground_task.add_task(rd.find_and_del, menu_id)
        # rd.del_key('menus')
        # rd.find_and_del(menu_id)
        return await self.dish_rep._delete_dish(submenu_id, dish_id)
