from __future__ import annotations

import os.path
from datetime import datetime
from typing import Optional, List

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Time, ForeignKey, func
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column, relationship
from sqlalchemy.types import PickleType
# Создаем базовый класс для объявления моделей
from sqlalchemy.orm import DeclarativeBase



# Определяем модель для таблицы Orders
class Base(DeclarativeBase):
   pass

meta = MetaData()
session = None

#Старый код
# association_table = Table(
# "Order_products",
# Base.metadata,
# Column("order_product_id", Integer, primary_key=True, autoincrement=True),
# Column("order_id", ForeignKey("Orders.order_id")),
# Column("product_id", ForeignKey("Products.product_id")),
# )
#
# class Products(Base):
#     __tablename__ = 'Products'
#     product_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     product_name: Mapped[str] = mapped_column(String(100), nullable=False)
#     category: Mapped[str] = mapped_column(String(100), nullable=False)
#     price: Mapped[int] = mapped_column(Integer, nullable=False)
#     orders: Mapped[List[Orders]] = relationship(
#         secondary=association_table, back_populates="products"
#     )
# class Orders(Base):
#     __tablename__ = 'Orders'
#     order_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     time_created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
#     time_updated: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())
#     client_id: Mapped[int] = mapped_column(Integer, ForeignKey('Clients.client_id'), nullable=False)
#     product_type: Mapped[object] = mapped_column(PickleType)
#
#     products: Mapped[List[Products]] = relationship(
#         secondary=association_table, back_populates="orders"
#     )

association_table = Table(
    "Order_products",
    Base.metadata,
    Column("order_product_id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", ForeignKey("Orders.order_id")),
    Column("product_id", ForeignKey("Products.product_id")),
    Column("product_obj_upd", PickleType)
)

class Products(Base):
    __tablename__ = 'Products'
    product_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    product_obj = Column(PickleType)
    orders = relationship("Orders", secondary=association_table, back_populates="products")

class Orders(Base):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    client_id = Column(Integer, ForeignKey('Clients.client_id'), nullable=False)


    products = relationship("Products", secondary=association_table, back_populates="orders")
class Clients(Base):
    __tablename__ = 'Clients'
    client_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=False)

class Sauces(Base):
    __tablename__ = 'Sauces'
    sauces_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    sauce_name: Mapped[str] = mapped_column(String, nullable=False)

class Fillings(Base):
    __tablename__ = 'Fillings'
    fillings_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    fillings_name: Mapped[str] = mapped_column(String, nullable=False)

class Dough(Base):
    __tablename__ = 'Dough'
    dough_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    dough_name: Mapped[str] = mapped_column(String, nullable=False)


class Category(Base):
    __tablename__ = 'Category'
    category_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    category_name: Mapped[str] = mapped_column(String, nullable=False)

def create_db():
    global session

    db_name = 'pizza'
    engine = create_engine(f'sqlite:///{db_name}.db', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    Base.metadata.create_all(engine)

def session_db():
    global session
    return session

create_db()