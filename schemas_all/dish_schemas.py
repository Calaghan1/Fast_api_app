import uuid

from pydantic import BaseModel


class Config(BaseModel):
    orm_mode = True


class ShowDishes(Config):
    id: uuid.UUID
    title: str
    description: str
    price: str


class Dishescrate(BaseModel):
    title: str
    description: str
    price: str
