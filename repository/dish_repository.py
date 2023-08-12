from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import database.models as models
from database.database import get_db
from schemas_all import dish_schemas
from sqlalchemy import delete, func, select, distinct, outerjoin

class DishesRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    async def _get_dishes(self, api_test_menu_id: str, submenu_id: str) -> list[dish_schemas.ShowDishes]:
        response = []
        dishes = await self.db.execute(select(models.Dishes.id, models.Dishes.title, models.Dishes.description,
                                              models.Dishes.price).where(models.Dishes.submenu_id == submenu_id))
        dishes = dishes.all()
        for d in dishes:
            print(d)
            response.append(dish_schemas.ShowDishes(id=d[0], title=d[1],
                                                    description=d[2], price=d[3]))
        return response

    async def _create_dish(self, dish: dish_schemas.Dishescrate, api_test_menu_id: str, api_test_submenu_id: str) -> dish_schemas.ShowDishes:
        db_menu = models.Dishes(title=dish.title, description=dish.description,
                                price=dish.price, submenu_id=api_test_submenu_id)
        self.db.add(db_menu)
        await self.db.commit()
        await self.db.refresh(db_menu)
        return dish_schemas.ShowDishes(id=db_menu.id, title=db_menu.title, description=db_menu.description, price=db_menu.price)

    async def _get_uniq_dish(self, api_test_dish_id: str) -> dish_schemas.ShowDishes:
        try:
            dish = await self.db.execute(select(models.Dishes.id, models.Dishes.title, models.Dishes.description,
                                              models.Dishes.price).where(models.Dishes.id == api_test_dish_id))
            dish = dish.one()
            print(dish)
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
        except Exception:
            raise HTTPException(status_code=404, detail='dish not found')
        return dish_schemas.ShowDishes(id=dish[0], title=dish[1], description=dish[2], price=dish[3])

    async def _update_dish(self, menu: dish_schemas.Dishescrate, api_test_menu_id: str, api_test_submenu_id: str, api_test_dish_id: str) -> dish_schemas.ShowDishes:
        try:
            dish = await self.db.execute(select(models.Dishes).where(models.Dishes.id == api_test_dish_id))
            dish = dish.one()
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
        except Exception:
            raise HTTPException(status_code=404, detail='dish not found')
        await self.db.execute(update(models.Dishes).where(models.Dishes.id == api_test_dish_id).values(title=menu.title, description=menu.description,
                                                                                          price=menu.price))
        await self.db.commit()
        return await self._get_uniq_dish(api_test_dish_id)

    async def _delete_dish(self, api_test_submenu_id: str, api_test_dish_id: str) -> dict:
        try:
            dish = await self.db.execute(select(models.Dishes).where(models.Dishes.id == api_test_dish_id))
            dish = dish.one()
            if not dish:
                raise HTTPException(status_code=404, detail='dish not found')
        except Exception:
            raise HTTPException(status_code=404, detail='dish not found')
        await self.db.execute(delete(models.Dishes).where(models.Dishes.id == api_test_dish_id))
        await self.db.commit()
        return {'status': True, 'message': 'The dish has been deleted'}
