import uuid

from pydantic import BaseModel


class Config(BaseModel):
    orm_mode = True


class MenuCreate(BaseModel):
    title: str
    description: str


class ShowMenu(Config):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class SubmenuCreate(BaseModel):
    title: str
    description: str


class ShowSubmenu(Config):
    id: uuid.UUID
    title: str
    description: str
    dishes_count: int


class ShowDishes(Config):
    id: uuid.UUID
    title: str
    description: str
    price: str


class Dishescrate(BaseModel):
    title: str
    description: str
    price: str
