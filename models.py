import uuid

from sqlalchemy import NUMERIC, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Menu(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    submenus = relationship('Submenu', backref='menu', cascade='all,delete', lazy='dynamic')

    @property
    def submenus_count(self):
        return self.submenus.count()

    @property
    def dishes_count(self):
        return sum(len(submenu.dishes) for submenu in self.submenus)


class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    dishes = relationship('Dishes', backref='submenu', cascade='all,delete')

    @property
    def dishes_count(self):
        return len(self.dishes)


class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(NUMERIC(10, 2))
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'))
