from fastapi import Depends

from database.redis_tools import rd
from repository.menu_repository import MenuRepository
from schemas_all import menu_schemas


class menu_service:
    def __init__(self, db: MenuRepository = Depends()) -> None:
        self.menu_rep = db

    def get_menu(self) -> list[menu_schemas.ShowMenu]:
        cache = rd.get_value('menus')
        if cache:
            print('cache')
            return cache
        else:
            result = self.menu_rep._get_menu()
            rd.set_pair('menus', result)
            return result

    def get_uniq_menu(self, menu_id: str) -> menu_schemas.ShowMenu:
        cache = rd.get_value(f'menus-{menu_id}')
        if cache:
            return cache
        else:
            result = self.menu_rep._get_uniq_menu(menu_id)
            rd.set_pair(f'menus-{menu_id}', result)
            return result

    def create_menu(self, data: menu_schemas.MenuCreate) -> menu_schemas.ShowMenu:
        rd.del_key('menus')
        return self.menu_rep._create_menu(data)

    def update_menu(self, menu_id: str, data: menu_schemas.MenuCreate) -> menu_schemas.ShowMenu:
        rd.del_key('menus')
        rd.del_key(f'menus-{menu_id}')
        return self.menu_rep._update_menu(data, menu_id)

    def delete_menu(self, menu_id: str) -> dict:
        rd.del_key('menus')
        rd.find_and_del(menu_id)
        return self.menu_rep._delete_menu(menu_id)
