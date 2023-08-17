import uuid

from pydantic import BaseModel

# class Config(BaseModel):
#     orm_mode = True


class SubmenuCreate(BaseModel):
    title: str
    description: str


class ShowSubmenu(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    dishes_count: int

    class ConfigDict:
        from_attributes = True
