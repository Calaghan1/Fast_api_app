from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import database.models as models
from database.database import get_db
from schemas_all import menu_schemas
from sqlalchemy import delete, func, select, distinct, outerjoin
from sqlalchemy.orm import selectinload
class MenuRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db

    async def _get_menu(self) -> list[menu_schemas.ShowMenu]:
        response = []
        menu = await self.db.execute(select(models.Menu.id, models.Menu.title, models.Menu.description, 
                                            func.count(distinct(models.Submenu.id).label('submenu_count')), 
                                            func.count(distinct(models.Dishes.id).label('dishes_count'))).outerjoin(
                                                models.Submenu, models.Menu.id == models.Submenu.menu_id).outerjoin(
                                                    models.Dishes, models.Dishes.submenu_id == models.Submenu.id
                                                ).group_by(models.Menu.id)
                                            )
        menus = menu.all()
        for m in menus:
            response.append(menu_schemas.ShowMenu(id=m[0], title=m[1], description=m[2],
                            submenus_count=str(m[3]), dishes_count=str(m[4])))
        return response

    async def _get_uniq_menu(self, menu_id: str) -> menu_schemas.ShowMenu:
        try:
            # m = self.db.query(models.Menu).filter(models.Menu.id == menu_id).first()
            m = await self.db.execute(select(models.Menu.id, models.Menu.title, models.Menu.description, 
                                            func.count(distinct(models.Submenu.id).label('submenu_count')), 
                                            func.count(distinct(models.Dishes.id).label('dishes_count'))).where(models.Menu.id == menu_id).outerjoin(
                                                models.Submenu, models.Menu.id == models.Submenu.menu_id).outerjoin(
                                                    models.Dishes, models.Dishes.submenu_id == models.Submenu.id
                                                ).group_by(models.Menu.id)
                                            )
            m = m.one()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        response = menu_schemas.ShowMenu(id=m[0], title=m[1], description=m[2],
                            submenus_count=str(m[3]), dishes_count=str(m[4]))
        return response

    async def _create_menu(self, menu: menu_schemas.MenuCreate) -> menu_schemas.ShowMenu:
        m = models.Menu(title=menu.title, description=menu.description)
        self.db.add(m)
        await self.db.commit()
        await self.db.refresh(m)
        return menu_schemas.ShowMenu(id=m.id, description=m.description, title=m.title, submenus_count = 0, dishes_count = 0)

    async def _update_menu(self, menu: menu_schemas.MenuCreate, api_test_menu_id: str) -> menu_schemas.ShowMenu:
        try:
            m = await self.db.execute(select(models.Menu).where(models.Menu.id == api_test_menu_id))
            m = m.one()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        res = await self.db.execute(update(models.Menu).where(models.Menu.id == api_test_menu_id).values(
            title=menu.title, description=menu.description))
        await self.db.commit()
        return await self._get_uniq_menu(api_test_menu_id)

    async def _delete_menu(self, api_test_menu_id: str) -> dict:
        try:
            m = await self.db.execute(select(models.Menu).where(models.Menu.id == api_test_menu_id))
            m =  m.one()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        await self.db.execute(delete(models.Menu).where(models.Menu.id == api_test_menu_id))
        await self.db.commit()
        return {'status': True, 'message': 'The menu has been deleted'}



    async def _get_all_data(self):
        result = await self.db.execute(
            select(models.Menu).options(
                selectinload(models.Menu.submenus).selectinload(models.Submenu.dishes)
            )
        )
        menus = result.scalars().all()
        return menus