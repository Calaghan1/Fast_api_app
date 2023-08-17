import json

from fastapi import FastAPI

from app.dishes_endpoints import dish_router
from app.menu_endpoints import menu_router
from app.submenu_endpoints import submenu_router
from database.database import create_tables

# models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(router=menu_router)
app.include_router(router=submenu_router)
app.include_router(router=dish_router)

list_or_routes = []

with open('openapi.json', 'w') as f:
    f.write(json.dumps(app.openapi()))

for route in app.routes:
    list_or_routes.append(route)


def reverse(name: str, values={}) -> str:
    for route in list_or_routes:
        if name == route.name:
            return route.path.format(**values)
    return ''


@app.on_event('startup')
async def set_up_base():
    await create_tables()
