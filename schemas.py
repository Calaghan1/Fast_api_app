from pydantic import BaseModel
import uuid

class Config(BaseModel):
        orm_mode = True
        
class MenuCreate(BaseModel):
    title:str
    description: str
    
class ShowMenu(Config):
    id: uuid.UUID
    title: str
    description: str


class SubmenuCreate(BaseModel):
    title:str
    description: str
    
    
class ShowSubmenu(Config):
    id: uuid.UUID
    title: str
    description: str
    

    
class ShowDishes(Config):
    id: uuid.UUID
    title: str
    description: str
    price: str

class Dishescrate(BaseModel):
    title: str
    description: str
    price: str
    
    
#     # SELECT count(*), (SELECT count(id) FROM submenus WHERE submenus.menu_id = menus.id)as submenus_count FROM menus;
    
    
#     # SELECT * FROM menus, submenus, dishes GROUP BY menus.id;
    
    
    
#     # SELECT 
    
#     SELECT 
#     m.*,
#     (
#         SELECT COUNT(*) 
#         FROM submenus sm 
#         WHERE sm.menu_id = m.id
#     ) as submenus_count,
#     (
#         SELECT COUNT(*) 
#         FROM dishes d 
#         WHERE EXISTS (SELECT * FROM submenus sm WHERE sm.menu_id = m.id AND sm.id = d.submenu_id)
#     ) as dishes_count
# FROM menus m;