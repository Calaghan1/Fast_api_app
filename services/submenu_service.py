from fastapi import Depends

from database.redis_tools import rd
from repository.submenu_repository import SubmenuRepository
from schemas_all import submenu_schemas


class submenus_service:
    def __init__(self, db: SubmenuRepository = Depends()) -> None:
        self.submenu_rep = db

    def get_submenu(self, menu_id: str) -> list[submenu_schemas.ShowSubmenu]:
        cache = rd.get_value(f'menus-{menu_id}:submenus')
        if cache:
            return cache
        else:
            result = self.submenu_rep._get_submenu(menu_id)
            rd.set_pair(f'menus-{menu_id}:submenus', result)
            return result

    def get_uniq_submenu(self, menu_id: str, submenu_id: str) -> submenu_schemas.ShowSubmenu:
        cache = rd.get_value(f'menus-{menu_id}:submenus-{submenu_id}')
        if cache:
            return cache
        else:
            result = self.submenu_rep._get_uniq_submenu(submenu_id)
            rd.set_pair(f'menus-{menu_id}:submenus-{submenu_id}', result)
            return result

    def create_submenu(self, menu_id: str, data: submenu_schemas.SubmenuCreate) -> submenu_schemas.ShowSubmenu:
        rd.del_key('menus')
        rd.find_and_del(menu_id)
        return self.submenu_rep._create_submenu(data, menu_id)

    def update_submenu(self, menu_id: str, submenu_id: str, data: submenu_schemas.SubmenuCreate) -> submenu_schemas.ShowSubmenu:
        rd.find_and_del(submenu_id)
        rd.del_key(f'menus-{menu_id}:submenus')
        return self.submenu_rep._update_submenu(data, submenu_id)

    def delete_submenu(self, menu_id: str, submenu_id: str) -> dict:
        rd.del_key('menus')
        rd.find_and_del(menu_id)
        return self.submenu_rep._delete_submenu(menu_id, submenu_id)
