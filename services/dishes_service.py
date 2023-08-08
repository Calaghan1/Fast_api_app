from fastapi import Depends

from database.redis_tools import rd
from repository.dish_repository import DishesRepository
from schemas_all import dish_schemas


class dishes_service:
    def __init__(self, db: DishesRepository = Depends()) -> None:
        self.dish_rep = db

    def get_dishes(self, menu_id: str, submenu_id: str) -> list[dish_schemas.ShowDishes]:
        cache = rd.get_value(f'menus-{menu_id}:submenu-{submenu_id}:dishes')
        if cache:
            return cache
        else:
            result = self.dish_rep._get_dishes(menu_id, submenu_id)
            rd.set_pair(f'menus-{menu_id}:submenu-{submenu_id}:dishse', result)
            return result

    def get_uniq_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> dish_schemas.ShowDishes:
        cache = rd.get_value(f'menus-{menu_id}:submenu-{submenu_id}:dishes-{dish_id}')
        if cache:
            return cache
        else:
            result = self.dish_rep._get_uniq_dish(dish_id)
            rd.set_pair(f'menus-{menu_id}:submenu-{submenu_id}:dishes-{dish_id}', result)
            return result

    def update_dish(self, menu_id: str, submenu_id: str, dish_id: str, data: dish_schemas.Dishescrate) -> dish_schemas.ShowDishes:
        rd.del_key(f'menus-{menu_id}:submenu-{submenu_id}:dishes')
        rd.find_and_del(dish_id)
        return self.dish_rep._update_dish(data, menu_id, submenu_id, dish_id)

    def create_dish(self, menu_id: str, submenu_id: str, data: dish_schemas.Dishescrate) -> dish_schemas.ShowDishes:
        rd.del_key('menus')
        rd.find_and_del(menu_id)
        return self.dish_rep._create_dish(data, menu_id, submenu_id)

    def delete_dish(self, menu_id: str, submenu_id: str, dish_id: str) -> dict:
        rd.del_key('menus')
        rd.find_and_del(menu_id)
        return self.dish_rep._delete_dish(submenu_id, dish_id)
