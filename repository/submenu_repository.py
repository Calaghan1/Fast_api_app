from fastapi import Depends, HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

import database.models as models
from database.database import get_db
from schemas_all import submenu_schemas
from sqlalchemy import delete, func, select, distinct, outerjoin

class SubmenuRepository:
    def __init__(self, db: Session = Depends(get_db)) -> None:
        self.db = db
        self.rd_submenus = 'submenus'

    async def _get_submenu(self, menu_id: str) -> list[submenu_schemas.ShowSubmenu]:
        try:
            m = await self.db.execute(select(models.Menu).where(models.Menu.id == menu_id))
            m = m.one()
            if not m:
                raise HTTPException(status_code=404, detail='menu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='menu not found')
        response = []
        submenus = await self.db.execute(select(models.Submenu.id, models.Submenu.title, models.Submenu.description,
                                                func.count(distinct(models.Dishes.id).label('dishes_count'))).where(
                                                    models.Submenu.menu_id == menu_id).outerjoin(models.Dishes, 
                                                         models.Dishes.submenu_id == models.Submenu.id).group_by(
                                                        models.Submenu.id))
        submenus = submenus.all()
        for m in submenus:
            response.append(submenu_schemas.ShowSubmenu(id=m[0], title=m[1],
                            description=m[2], dishes_count=m[3]))
        return response

    async def _get_uniq_submenu(self, menu_id: str, api_test_submenu_id: str) -> submenu_schemas.ShowSubmenu:
        try:
            submenus = await self.db.execute(select(models.Submenu.id, models.Submenu.title, models.Submenu.description,
                                                func.count(distinct(models.Dishes.id).label('dishes_count'))).where(
                                                    models.Submenu.menu_id == menu_id).outerjoin(models.Dishes, 
                                                         models.Dishes.submenu_id == models.Submenu.id).group_by(
                                                        models.Submenu.id))
            submenus = submenus.one()
            if not submenus:
                raise HTTPException(status_code=404, detail='submenu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='submenu not found')
        response = submenu_schemas.ShowSubmenu(id=submenus[0], title=submenus[1],
                            description=submenus[2], dishes_count=submenus[3])
        return response

    async def _create_submenu(self, menu: submenu_schemas.SubmenuCreate, menu_id: str) -> submenu_schemas.ShowSubmenu:
        m = models.Submenu(title=menu.title, description=menu.description, menu_id=menu_id)
        self.db.add(m)
        await self.db.commit()
        await self.db.refresh(m)
        return submenu_schemas.ShowSubmenu(id=m.id, description=m.description, title=m.title, dishes_count=0)

    async def _update_submenu(self, menu: submenu_schemas.SubmenuCreate, menu_id: str, api_test_submenu_id: str) -> submenu_schemas.ShowSubmenu:
        try:
            m = await self.db.execute(select(models.Submenu).where(models.Submenu.id == api_test_submenu_id))
            m = m.one()
            if not m:
                raise HTTPException(status_code=404, detail='submenu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='submenu not found')
        res = await self.db.execute(update(models.Submenu).where(models.Submenu.id == api_test_submenu_id).values(
            title=menu.title, description=menu.description))
        await self.db.commit()
        return await self._get_uniq_submenu(menu_id, api_test_submenu_id)

    async def _delete_submenu(self, menu_id: str, submenu_id: str) -> dict:
        try:
            m = await self.db.execute(select(models.Submenu).where(models.Submenu.id == submenu_id))
            m = m.one()
            if not m:
                raise HTTPException(status_code=404, detail='submenu not found')
        except Exception:
            raise HTTPException(status_code=404, detail='submenu not found')
        await self.db.execute(delete(models.Submenu).where(models.Submenu.id == submenu_id))
        await self.db.commit()
        return {'status': True, 'message': 'The submenu has been deleted'}
