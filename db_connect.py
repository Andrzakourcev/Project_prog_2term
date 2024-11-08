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


class Orders(Base):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    client_id = Column(Integer, ForeignKey('Clients.client_id'), nullable=False)
    order_products = relationship("Order_products", back_populates="order")

class Order_products(Base):
    __tablename__ = 'Order_products'
    order_product_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('Orders.order_id'))
    product_info = Column(PickleType)
    order = relationship("Orders", back_populates="order_products")

class Products(Base):
    __tablename__ = 'Products'
    product_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    product_name = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    type_product = Column(PickleType)


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
#

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

    # fillings_id = 1
    #
    # # Запрос с использованием метода query и фильтрацией по fillings_id
    # result = session.query(Products).filter(Products.c.product_id == fillings_id).one()
    # print(result)

def session_db():
    global session
    return session

create_db()