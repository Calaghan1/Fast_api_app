import uuid

from pydantic import BaseModel


# class Config(BaseModel):
#     orm_mode = True


class ShowDishes(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: str
    
    class ConfigDict:
        from_attributes = True

class Dishescrate(BaseModel):
    title: str
    description: str
    price: str
