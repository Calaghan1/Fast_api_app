import uuid

from pydantic import BaseModel

# class Config(BaseModel):
#     orm_mode = True


class MenuCreate(BaseModel):
    title: str
    description: str


class ShowMenu(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    class ConfigDict:
        from_attributes = True
