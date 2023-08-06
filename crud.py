from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import models
import schemas
from database import SessionLocal
from redis_tools import RedisTools

rd = RedisTools()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
                response.append(schemas.ShowMenu(id=m.id, description=m.description, title=m.title,
                                submenus_count=m.submenus_count, dishes_count=m.dishes_count))
            rd.set_pair(self.rd_menus, response)
            return response

    def _get_uniq_menu(self, menu_id: str) -> schemas.ShowMenu:
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
            response = schemas.ShowMenu(id=m.id, description=m.description, title=m.title,
                                        submenus_count=m.submenus_count, dishes_count=m.dishes_count)
            rd.set_pair(self.rd_menus + str(menu_id), response)
            return response

    def _create_menu(self, menu: schemas.MenuCreate) -> schemas.ShowMenu:
        m = models.Menu(title=menu.title, description=menu.description)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        # rd.del_key(self.rd_menus)
        rd.del_all()
        return schemas.ShowMenu(id=m.id, description=m.description, title=m.title, submenus_count=m.submenus_count, dishes_count=m.dishes_count)

    def _update_menu(self, menu: schemas.MenuCreate, api_test_menu_id: str) -> schemas.ShowMenu:
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


class SubmenuRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.rd_submenus = 'submenus'

    def _get_submenu(self, menu_id: str) -> list[schemas.ShowSubmenu]:
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
                response.append(schemas.ShowSubmenu(id=m.id, description=m.description,
                                title=m.title, dishes_count=m.dishes_count))
            rd.set_pair(self.rd_submenus, response)
        return response

    def _get_uniq_submenu(self, api_test_submenu_id: str) -> schemas.ShowSubmenu:
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
            response = schemas.ShowSubmenu(id=m.id, description=m.description,
                                           title=m.title, dishes_count=m.dishes_count)
            rd.set_pair(self.rd_submenus + api_test_submenu_id, response)
            return response

    def _create_submenu(self, menu: schemas.SubmenuCreate, menu_id: str) -> schemas.ShowSubmenu:
        # rd.del_key(self.rd_submenus)
        rd.del_all()
        m = models.Submenu(title=menu.title, description=menu.description, menu_id=menu_id)
        self.db.add(m)
        self.db.commit()
        self.db.refresh(m)
        return schemas.ShowSubmenu(id=m.id, description=m.description, title=m.title, dishes_count=m.dishes_count)

    def _update_submenu(self, menu: schemas.SubmenuCreate, api_test_submenu_id: str) -> schemas.ShowSubmenu:
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


class DishesRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.rd_dishes = 'dishes'

    def _get_dishes(self, api_test_menu_id: str, api_test_submenu_id: str) -> list[schemas.ShowDishes]:
        cache = rd.get_value(self.rd_dishes)
        if cache:
            return cache
        else:
            response = self.db.query(models.Dishes).filter(models.Dishes.submenu_id == api_test_submenu_id).all()
            rd.set_pair(self.rd_dishes, response)
            return response

    def _create_dish(self, dish: schemas.Dishescrate, api_test_menu_id: str, api_test_submenu_id: str) -> schemas.ShowSubmenu:
        rd.del_key(self.rd_dishes)
        db_menu = models.Dishes(title=dish.title, description=dish.description,
                                price=dish.price, submenu_id=api_test_submenu_id)
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return schemas.ShowDishes(id=db_menu.id, title=db_menu.title, description=db_menu.description, price=db_menu.price)

    def _get_uniq_dish(self, api_test_dish_id: str) -> schemas.ShowSubmenu:
        cache = rd.get_value(self.rd_dishes + api_test_dish_id)
        if cache:
            return cache
        else:
            try:
                dish = self.db.query(models.Dishes).filter(models.Dishes.id == api_test_dish_id).first()
                if not dish:
                    raise HTTPException(status_code=404, detail='dish not found')
            except Exception:
                raise HTTPException(status_code=404, detail='dish not found')
            rd.set_pair(self.rd_dishes + api_test_dish_id, dish)
            return schemas.ShowDishes(id=dish.id, title=dish.title, description=dish.description, price=dish.price)

    def _update_dish(self, menu: schemas.SubmenuCreate, api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str) -> schemas.ShowSubmenu:
        try:
            dish = self.db.query(models.Dishes).filter(models.Dishes.id == api_test_dish_id).all()
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
        except Exception:
            raise HTTPException(status_code=404, detail='dish not found')
        # rd.del_key(self.rd_dishes)
        # rd.del_key(self.rd_dishes+api_test_dish_id)
        rd.del_all()
        query = update(models.Dishes).where(models.Dishes.id == api_test_dish_id).values(title=menu.title, description=menu.description,
                                                                                         price=menu.price).returning(models.Dishes.id, models.Dishes.title, models.Dishes.description, models.Dishes.price)
        self.db.execute(query)
        self.db.commit()
        dish = self.db.query(models.Dishes).filter(models.Dishes.id == api_test_dish_id).first()
        return schemas.ShowDishes(id=dish.id, title=dish.title, description=dish.description, price=dish.price)

    def _delete_dish(self, api_test_submenu_id: str, api_test_dish_id: str) -> dict:
        try:
            dish = self.db.query(models.Dishes).filter(models.Dishes.id == api_test_dish_id).all()
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
        except Exception:
            raise HTTPException(status_code=404, detail='dish not found')
        # rd.del_key(self.rd_dishes)
        # rd.del_key(self.rd_dishes+api_test_dish_id)
        rd.del_all()
        query = self.db.query(models.Dishes).filter(models.Dishes.id == api_test_dish_id,
                                                    models.Dishes.submenu_id == api_test_submenu_id).first()
        self.db.delete(query)
        self.db.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
