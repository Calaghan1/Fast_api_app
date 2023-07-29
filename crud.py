from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import text, update, delete
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
import models, schemas
import json
import uu

from sqlalchemy import select
def get_nums_for_menu(db: Session, menu_id):
    count_of_submenus = 0
    count_of_dishes = 0
    for submenu in db.query(models.Submenu).filter(models.Submenu.menu_id==menu_id).all():
            count_of_submenus += 1
            submenu_d = submenu.__dict__
            count_of_dishes = len(db.query(models.Dishes).filter(models.Dishes.submenu_id==submenu_d['id']).all())
    return (count_of_submenus,count_of_dishes)



    
#menu
def _get_menu(db: Session):
    response = []
    for u in db.query(models.Menu).all():
        menu_d = u.__dict__
        submenu_and_dishes = get_nums_for_menu(db, menu_d['id'])
        menu_d['submenus_count'] = submenu_and_dishes[0]
        menu_d['dishes_count'] = submenu_and_dishes[1]
        response.append(menu_d)
    # # query = db.query(models.Menu, 
    # #                   func.count(models.Submenu.id).label("submenus_count"), 
    # #                   func.sum(func.count(models.Dishes.id)).label("dishes_count")
    # #                  ).select_from(models.Menu
    # #                  ).outerjoin(models.Submenu
    # #                  ).outerjoin(models.Dishes
    # #                  ).group_by(models.Menu.id)
    # query = db.query(
    # models.Menu,
    # func.count(models.Submenu.id).label("submenus_count"),
    # func.sum(func.case([(models.Dishes.id != None, 1)], else_=0)).label("dishes_count")
    # ).\
    # outerjoin(models.Submenu).\
    # outerjoin(models.Dishes).\
    # group_by(models.Menu.id)

    return response

def _get_uniq_menu(db:Session, menu_id):
    # menu_id = uu.encode(menu_id, False)
    response = []
    for u in db.query(models.Menu).filter(models.Menu.id==menu_id).all():
        menu_d = u.__dict__
        submenu_and_dishes = get_nums_for_menu(db, menu_d['id'])
        menu_d['submenus_count'] = submenu_and_dishes[0]
        menu_d['dishes_count'] = submenu_and_dishes[1]
        response.append(menu_d)
    print(response)
    return response[0]

def _create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(title=menu.title, description=menu.description)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    menus_d = dict(schemas.ShowMenu(id=db_menu.id, title=db_menu.title, description=db_menu.description))
    submenu_and_dishes = get_nums_for_menu(db, menus_d['id'])
    menus_d['submenus_count'] = submenu_and_dishes[0]
    menus_d['dishes_count'] = submenu_and_dishes[1]
    return menus_d


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
    count_of_dishes = 0
    for q in db.query(models.Submenu).filter(models.Submenu.menu_id==menu_id).all():
        sub_menu = q.__dict__
        count_of_dishes = len(db.query(models.Dishes).filter(models.Dishes.submenu_id==sub_menu['id']).all())
        sub_menu['dishes_count'] = count_of_dishes
        response.append(sub_menu)
    return response


def _get_uniq_submenu(db:Session, api_test_submenu_id):
    response = []
    count_of_dishes = 0 
    for q in db.query(models.Submenu).filter(models.Submenu.id==api_test_submenu_id).all():
        sub_menu = q.__dict__
        count_of_dishes = len(db.query(models.Dishes).filter(models.Dishes.submenu_id==sub_menu['id']).all())
        sub_menu['dishes_count'] = count_of_dishes
        response.append(sub_menu)
    return response[0]

    
def _create_submenu(db: Session, menu: schemas.SubmenuCreate, menu_id):
    db_menu = models.Submenu(title=menu.title, description=menu.description, menu_id=menu_id)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return schemas.ShowSubmenu(id=db_menu.id, title=db_menu.title, description=db_menu.description)

def _update_submenu(db: Session, menu: schemas.SubmenuCreate, api_test_menu_id, api_test_submenu_id):
    query = update(models.Submenu).where(models.Submenu.id == api_test_submenu_id).values(title=menu.title, description=menu.description).returning(models.Submenu.id, models.Submenu.title, models.Submenu.description)
    res = db.execute(query)
    db.commit()
    updated_menu = db.query(models.Submenu).filter(models.Submenu.id==api_test_submenu_id).first()
    print(updated_menu.__dict__)
    
    return updated_menu

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
