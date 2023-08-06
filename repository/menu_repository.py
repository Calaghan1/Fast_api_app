from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import database.models as models
from database.database import get_db
from database.redis_tools import rd
from schemas_all import menu_schemas


class MenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.rd_menus = 'menus'

    def _get_menu(self):
        cache = rd.get_value(self.rd_menus)
        if cache:
            return cache
        else:
            response = []
            menu = self.db.query(models.Menu).all()
            for m in menu:
                response.append(menu_schemas.ShowMenu(id=m.id, description=m.description, title=m.title,
                                submenus_count=m.submenus_count, dishes_count=m.dishes_count))
            rd.set_pair(self.rd_menus, response)
            return response

    def _get_uniq_menu(self, menu_id: str) -> menu_schemas.ShowMenu:
        cache = rd.get_value(self.rd_menus + str(menu_id))
        if cache:
            return cache
        else:
            try:
                m = self.db.query(models.Menu).filter(models.Menu.id == menu_id).first()
                if not m:
                    raise HTTPException(status_code=404, detail='menu not found')
            except Exception:
                raise HTTPException(status_code=404, detail='menu not found')
            response = menu_schemas.ShowMenu(id=m.id, description=m.description, title=m.title,
                                             submenus_count=m.submenus_count, dishes_count=m.dishes_count)
            rd.set_pair(self.rd_menus + str(menu_id), response)
            return response

    def _create_menu(self, menu: menu_schemas.MenuCreate) -> menu_schemas.ShowMenu:
        m = models.Menu(title=menu.title, description=menu.description)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        # rd.del_key(self.rd_menus)
        rd.del_all()
        return menu_schemas.ShowMenu(id=m.id, description=m.description, title=m.title, submenus_count=m.submenus_count, dishes_count=m.dishes_count)

    def _update_menu(self, menu: menu_schemas.MenuCreate, api_test_menu_id: str) -> menu_schemas.ShowMenu:
        try:
            m = self.db.query(models.Menu).filter(models.Menu.id == api_test_menu_id).all()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        # rd.del_key(self.rd_menus)
        # rd.del_key(self.rd_menus + str(api_test_menu_id))
        rd.del_all()
        query = update(models.Menu).where(models.Menu.id == api_test_menu_id).values(
            title=menu.title, description=menu.description).returning(models.Menu.id, models.Menu.title, models.Menu.description)
        res = self.db.execute(query)
        updated_menu = res.fetchone()[0]
        self.db.commit()
        return self._get_uniq_menu(updated_menu)

    def _delete_menu(self, api_test_menu_id: str) -> dict:
        try:
            m = self.db.query(models.Menu).filter(models.Menu.id == api_test_menu_id).all()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        # rd.del_key(self.rd_menus)
        # rd.del_key(self.rd_menus+api_test_menu_id)
        rd.del_all()
        query = self.db.query(models.Menu).filter(models.Menu.id == api_test_menu_id)
        query.delete()
        self.db.commit()
        return {'status': True, 'message': 'The menu has been deleted'}
