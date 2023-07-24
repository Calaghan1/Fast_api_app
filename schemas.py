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