from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import database.models as models
from database.database import get_db
from database.redis_tools import rd
from schemas_all import dish_schemas


class DishesRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self.rd_dishes = 'dishes'

    def _get_dishes(self, api_test_menu_id: str, api_test_submenu_id: str) -> list[dish_schemas.ShowDishes]:

        cache = rd.get_value(self.rd_dishes)
        if cache:
            return cache
        else:
            response = []
            for d in self.db.query(models.Dishes).filter(models.Dishes.submenu_id == api_test_submenu_id).all():
                response.append(dish_schemas.ShowDishes(id=d.id, title=d.title,
                                description=d.description, price=d.price))
            rd.set_pair(self.rd_dishes, response)
            return response

    def _create_dish(self, dish: dish_schemas.Dishescrate, api_test_menu_id: str, api_test_submenu_id: str) -> dish_schemas.ShowDishes:
        rd.del_key(self.rd_dishes)
        db_menu = models.Dishes(title=dish.title, description=dish.description,
                                price=dish.price, submenu_id=api_test_submenu_id)
        self.db.add(db_menu)
        self.db.commit()
        self.db.refresh(db_menu)
        return dish_schemas.ShowDishes(id=db_menu.id, title=db_menu.title, description=db_menu.description, price=db_menu.price)

    def _get_uniq_dish(self, api_test_dish_id: str) -> dish_schemas.ShowDishes:
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
            return dish_schemas.ShowDishes(id=dish.id, title=dish.title, description=dish.description, price=dish.price)

    def _update_dish(self, menu: dish_schemas.Dishescrate, api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str) -> dish_schemas.ShowDishes:
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
        return dish_schemas.ShowDishes(id=dish.id, title=dish.title, description=dish.description, price=dish.price)

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
