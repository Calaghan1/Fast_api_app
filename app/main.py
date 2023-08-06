from fastapi import FastAPI

import models
from app.dishes_endpoints import dish_router
from app.menu_endpoints import menu_router
from app.submenu_endpoints import submenu_router
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(router=menu_router)
app.include_router(router=submenu_router)
app.include_router(router=dish_router)
