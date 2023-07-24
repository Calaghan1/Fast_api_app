from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, NUMERIC
from sqlalchemy.orm import relationship
from database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Menu(Base):
    __tablename__ = 'menus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    submenus = relationship("Submenu", backref="menu", cascade="all,delete")
    
class Submenu(Base):
    __tablename__ = 'submenus'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    dishes = relationship("Dishes", backref="submenu", cascade="all,delete")
    
    # menu = relationship('Menu', backref='id')
    
class Dishes(Base):
    __tablename__ = 'dishes'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(NUMERIC(10,2))
    SubMenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))