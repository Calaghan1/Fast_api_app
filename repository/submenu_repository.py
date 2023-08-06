from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import database.models as models
from database.database import get_db
from database.redis_tools import rd
from schemas_all import submenu_schemas


class SubmenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.rd_submenus = 'submenus'

    def _get_submenu(self, menu_id: str) -> list[submenu_schemas.ShowSubmenu]:
        try:
            m = self.db.query(models.Menu).filter(models.Menu.id == menu_id).first()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        cache = rd.get_value(self.rd_submenus)
        if cache:
            return cache
        else:
            response = []
            for m in self.db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).all():
                response.append(submenu_schemas.ShowSubmenu(id=m.id, description=m.description,
                                title=m.title, dishes_count=m.dishes_count))
            rd.set_pair(self.rd_submenus, response)
        return response

    def _get_uniq_submenu(self, api_test_submenu_id: str) -> submenu_schemas.ShowSubmenu:
        try:
            m = self.db.query(models.Submenu).filter(models.Submenu.id == api_test_submenu_id).first()
            if not m:
                raise HTTPException(status_code=404, detail='submenu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='submenu not found')
        cache = rd.get_value(self.rd_submenus + api_test_submenu_id)
        if cache:
            return cache
        else:
            response = submenu_schemas.ShowSubmenu(id=m.id, description=m.description,
                                                   title=m.title, dishes_count=m.dishes_count)
            rd.set_pair(self.rd_submenus + api_test_submenu_id, response)
            return response

    def _create_submenu(self, menu: submenu_schemas.SubmenuCreate, menu_id: str) -> submenu_schemas.ShowSubmenu:
        # rd.del_key(self.rd_submenus)
        rd.del_all()
        m = models.Submenu(title=menu.title, description=menu.description, menu_id=menu_id)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return submenu_schemas.ShowSubmenu(id=m.id, description=m.description, title=m.title, dishes_count=m.dishes_count)

    def _update_submenu(self, menu: submenu_schemas.SubmenuCreate, api_test_submenu_id: str) -> submenu_schemas.ShowSubmenu:
        try:
            m = self.db.query(models.Submenu).filter(models.Submenu.id == api_test_submenu_id).first()
            if not m:
                raise HTTPException(status_code=404, detail='submenu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='submenu not found')
        # rd.del_key(self.rd_submenus)
        # rd.del_key(self.rd_submenus+api_test_submenu_id)
        rd.del_all()
        query = update(models.Submenu).where(models.Submenu.id == api_test_submenu_id).values(
            title=menu.title, description=menu.description).returning(models.Submenu.id, models.Submenu.title, models.Submenu.description)
        self.db.execute(query)
        self.db.commit()
        return self._get_uniq_submenu(api_test_submenu_id)

    def _delete_submenu(self, api_test_menu_id: str, api_test_submenu_id: str) -> dict:
        try:
            m = self.db.query(models.Submenu).filter(models.Submenu.id == api_test_submenu_id).first()
            if not m:
                raise HTTPException(status_code=404, detail='submenu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='submenu not found')
        # rd.del_key(self.rd_submenus)
        # rd.del_key(self.rd_submenus+api_test_submenu_id)
        rd.del_all()
        query = self.db.query(models.Submenu).filter(models.Submenu.id == api_test_submenu_id,
                                                     models.Submenu.menu_id == api_test_menu_id).first()
        self.db.delete(query)
        self.db.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
