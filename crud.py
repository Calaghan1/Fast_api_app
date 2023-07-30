from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import text, update, delete
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
import models, schemas
import json
import uu

from sqlalchemy import select

#menu
def _get_menu(db: Session):
    response = []
    menu = db.query(models.Menu).all()
    for m in menu:
        response.append(schemas.ShowMenu(id=m.id, description=m.description, title=m.title, submenus_count=m.submenus_count, dishes_count=m.dishes_count))
    return response

def _get_uniq_menu(db:Session, menu_id):
    # menu_id = uu.encode(menu_id, False)
    m = db.query(models.Menu).filter(models.Menu.id==menu_id).first()
    return  schemas.ShowMenu(id=m.id, description=m.description, title=m.title, submenus_count=m.submenus_count, dishes_count=m.dishes_count)

def _create_menu(db: Session, menu: schemas.MenuCreate):
    m = models.Menu(title=menu.title, description=menu.description)
    db.add(m)
    db.commit()
    db.refresh(m)
    return schemas.ShowMenu(id=m.id, description=m.description, title=m.title, submenus_count=m.submenus_count, dishes_count=m.dishes_count)


def _update_menu(db: Session, menu: schemas.MenuCreate, api_test_menu_id):
    # db.query(models.Menu).filter(models.Menu.id == api_test_menu_id).update(menu)
    query = update(models.Menu).where(models.Menu.id == api_test_menu_id).values(title=menu.title, description=menu.description).returning(models.Menu.id, models.Menu.title, models.Menu.description)
    res = db.execute(query)
    updated_menu = res.fetchone()[0]
    db.commit()
    return _get_uniq_menu(db, updated_menu)
    
def _delete_menu(db: Session, api_test_menu_id):
    query = db.query(models.Menu).filter(models.Menu.id == api_test_menu_id)
    query.delete()
    db.commit()
    return {"status": True, "message":"The menu has been deleted"}
    



#submenu
def _get_submenu(db:Session, menu_id):
    response = []
    for m in db.query(models.Submenu).filter(models.Submenu.menu_id==menu_id).all():
        response.append(schemas.ShowSubmenu(id=m.id, description=m.description, title=m.title, dishes_count=m.dishes_count))
    return response


def _get_uniq_submenu(db:Session, api_test_submenu_id):
    response = []
    count_of_dishes = 0 
    m = db.query(models.Submenu).filter(models.Submenu.id==api_test_submenu_id).first()
  
    return schemas.ShowSubmenu(id=m.id, description=m.description, title=m.title, dishes_count=m.dishes_count)

    
def _create_submenu(db: Session, menu: schemas.SubmenuCreate, menu_id):
    m = models.Submenu(title=menu.title, description=menu.description, menu_id=menu_id)
    db.add(m)
    db.commit()
    db.refresh(m)
    return schemas.ShowSubmenu(id=m.id, description=m.description, title=m.title, dishes_count=m.dishes_count)

def _update_submenu(db: Session, menu: schemas.SubmenuCreate, api_test_menu_id, api_test_submenu_id):
    query = update(models.Submenu).where(models.Submenu.id == api_test_submenu_id).values(title=menu.title, description=menu.description).returning(models.Submenu.id, models.Submenu.title, models.Submenu.description)
    db.execute(query)
    db.commit()
    return _get_uniq_submenu(db, api_test_submenu_id)

def _delete_submenu(db: Session, api_test_menu_id, api_test_submenu_id):
    query = db.query(models.Submenu).filter(models.Submenu.id == api_test_submenu_id, models.Submenu.menu_id ==api_test_menu_id).first()
    db.delete(query)
    db.commit()
    return {"status": True, "message":"The menu has been deleted"}



#dishes
def _get_dishes(db: Session, api_test_menu_id, api_test_submenu_id):
    return db.query(models.Dishes).filter(models.Dishes.submenu_id==api_test_submenu_id).all()

def _create_dish(db: Session, dish: schemas.Dishescrate, api_test_menu_id, api_test_submenu_id):
    db_menu = models.Dishes(title=dish.title, description=dish.description, price=dish.price, submenu_id=api_test_submenu_id)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return schemas.ShowDishes(id=db_menu.id, title=db_menu.title, description=db_menu.description, price=db_menu.price)

def _update_dish(db: Session, menu: schemas.SubmenuCreate, api_test_menu_id, api_test_submenu_id, api_test_dish_id):
    query = update(models.Dishes).where(models.Dishes.id == api_test_dish_id).values(title=menu.title, description=menu.description, price=menu.price).returning(models.Dishes.id, models.Dishes.title, models.Dishes.description, models.Dishes.price)
    res = db.execute(query)
    db.commit()
    updated_menu = db.query(models.Dishes).filter(models.Dishes.id==api_test_dish_id).first()
    return updated_menu.__dict__

def _delete_dish(db: Session, api_test_submenu_id, api_test_dish_id):
    query = db.query(models.Dishes).filter(models.Dishes.id == api_test_dish_id, models.Dishes.submenu_id ==api_test_submenu_id).first()
    db.delete(query)
    db.commit()
    return {"status": True, "message":"The menu has been deleted"}
