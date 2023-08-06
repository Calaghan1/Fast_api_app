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
