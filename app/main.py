from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import uvicorn
from sqlalchemy import text




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

  
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#menus
@app.get('/api/v1/menus')
def get_menu(db:Session = Depends(get_db)):
    return crud._get_menu(db)




@app.post("/api/v1/menus", status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
        return crud._create_menu(db=db, menu=menu)



@app.get('/api/v1/menus/{target_menu_id}')
def get_uniq_menu(target_menu_id, db:Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Menu).filter(models.Menu.id==target_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="menu not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="menu not found")
    menu_qr = crud._get_uniq_menu(db, target_menu_id)
    return menu_qr
    
    
@app.patch('/api/v1/menus/{api_test_menu_id}')
def update_menu(menu: schemas.MenuCreate, api_test_menu_id, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Menu).filter(models.Menu.id==api_test_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="menu not found")
    print(menu_qr)
    if not menu_qr:
         raise HTTPException(status_code=404, detail="menu not found")
 
    return crud._update_menu(db, menu, api_test_menu_id)

@app.delete('/api/v1/menus/{api_test_menu_id}')
def delete_menu(api_test_menu_id, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Menu).filter(models.Menu.id==api_test_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="menu not found")
    # print(menu_qr)
    if not menu_qr:
         raise HTTPException(status_code=404, detail="menu not found")
 
    return crud._delete_menu(db, api_test_menu_id)




#submenu
@app.get('/api/v1/menus/{target_menu_id}/submenus')
def get_submenu(target_menu_id, db:Session = Depends(get_db)):
    return crud._get_submenu(db, menu_id=target_menu_id)

@app.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def get_uniq_submenu(api_test_menu_id, api_test_submenu_id, db:Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Submenu).filter(models.Submenu.id==api_test_submenu_id, models.Submenu.menu_id==api_test_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="submenu not found")
    return crud._get_uniq_submenu(db, api_test_submenu_id)



@app.post('/api/v1/menus/{target_menu_id}/submenus',response_model=schemas.ShowSubmenu, status_code=201)
def create_submenu(target_menu_id, submenu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    try:
         menu_qr = db.query(models.Menu).filter(models.Menu.id==target_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="menu not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="menu not found")     
    return crud._create_submenu(db, menu=submenu, menu_id=target_menu_id)        

@app.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def update_submenu(api_test_menu_id, api_test_submenu_id, menu: schemas.SubmenuCreate, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Submenu).filter(models.Submenu.id==api_test_submenu_id, models.Submenu.menu_id==api_test_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    if not menu_qr:
         raise HTTPException(status_code=404, detail="submenu not found")
 
    return crud._update_submenu(db, menu, api_test_menu_id, api_test_submenu_id)

@app.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
def delete_submenu(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Submenu).filter(models.Submenu.id==api_test_submenu_id, models.Submenu.menu_id==api_test_menu_id).all()
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="submenu not found")
    return crud._delete_submenu(db, api_test_menu_id, api_test_submenu_id)
        
        
#dishes
@app.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
def get_dishes(api_test_menu_id, api_test_submenu_id, db: Session = Depends(get_db)):
    try:        
        return crud._get_dishes(db,api_test_menu_id, api_test_submenu_id)
    except:
        raise HTTPException(status_code=404, detail="dish not found")


@app.get('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def get_uniq_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Dishes).filter(models.Dishes.id==api_test_dish_id).all()
    except:
        raise HTTPException(status_code=404, detail="dish not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="dish not found")
    dish = menu_qr[0].__dict__
    dish['price'] = str(dish['price'])
    return  dish


@app.post('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes', status_code=201)
def create_dish(api_test_menu_id, api_test_submenu_id, dish: schemas.Dishescrate, db: Session = Depends(get_db)):
    return crud._create_dish(db, dish, api_test_menu_id, api_test_submenu_id)


@app.patch('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def update_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, dish: schemas.Dishescrate, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Dishes).filter(models.Dishes.id==api_test_dish_id, models.Dishes.submenu_id ==api_test_submenu_id).all()
    except:
        raise HTTPException(status_code=404, detail="submenu not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="dish not found")
    dish = dict(crud._update_dish(db, dish,  api_test_menu_id, api_test_submenu_id, api_test_dish_id))
    dish['price'] = str(dish['price'])
    return dish

@app.delete('/api/v1/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
def del_dish(api_test_menu_id, api_test_submenu_id, api_test_dish_id, db: Session = Depends(get_db)):
    try:
        menu_qr = db.query(models.Dishes).filter(models.Dishes.id==api_test_dish_id).all()
    except:
        raise HTTPException(status_code=404, detail="dish not found")
    if not menu_qr:
        raise HTTPException(status_code=404, detail="dish not found")    
    return crud._delete_dish(db, api_test_submenu_id, api_test_dish_id)


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)