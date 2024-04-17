import os
from abc import ABC, abstractmethod
from datetime import time, datetime
import db_connect
import Exceptions
from db_connect import Clients, Orders, Sauces, Dough, Fillings, Products
import time


class Mixin_Spicy:
    @staticmethod
    def attention():
        print("Это пицца острая!!!!!")


class Pizza(ABC):
    name = None

    def __init__(self, dough=None, sauce=None, filling=None, size=None):
        self.__dough = dough
        self.__sauce = sauce
        self.__filling = filling
        self.__size = size

    @abstractmethod
    def get_size(self):
        return self.__size

    # def __repr__(self):
    #     return f"------------------- \n Название: {self.name} \n Состав: \n Тесто: {self.dough} \n Добавка: {self.filling} \n Соус: {self.sauce} \n Размер: {self.__size} \n -------------------"

    def track_time(f):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = f(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Прошло {execution_time} секунд")
            return result

        return wrapper

    # Сравнение пицц по тесту
    def __eq__(self, other):
        if isinstance(other, Pizza):
            return self.__size == other.__size
        return False

    def __lt__(self, other):
        if isinstance(other, Pizza):
            return self.__size < other.__size
        return False

    @property
    def dough(self):
        return self.__dough

    @dough.setter
    def dough(self, dough):
        self.__dough = dough

    @property
    def sauce(self):
        return self.__sauce

    @sauce.setter
    def sauce(self, sauce):
        self.__sauce = sauce

    @property
    def filling(self):
        return self.__filling

    @filling.setter
    def filling(self, filling):
        self.__filling = filling

    @track_time
    def make_pizza(self):
        time.sleep(2)
        print(f"Замешено тесто для пиццы {self.name}")
        time.sleep(2)
        print("Подготовились ингредиенты")
        time.sleep(2)
        print("Пицца испеклась")
        time.sleep(1)
        print("Пицца нарезалась")
        time.sleep(1)
        print("Пицца упаковалась")


class BBQ_Pizza(Pizza, Mixin_Spicy):
    name = 'Барбекю'

    def __init__(self):
        super().__init__(dough="Thin", sauce="Soy", filling="Beef", size=25)

    def get_size(self):
        super().get_size()


class Pepperoni(Pizza, Mixin_Spicy):
    name = 'Пепперони'

    def __init__(self):
        super().__init__(dough="Thick", sauce="Tomato sauce", filling="Pepperoni sausage", size=30)

    def get_size(self):
        super().get_size()
        print('Вызван абстрактный метод в Pepperoni')


class Seafood(Pizza):
    name = 'Дары моря'

    def __init__(self):
        super().__init__(dough="Medium", sauce="Cream sauce", filling="Squid", size=35)

    def get_size(self):
        super().get_size()
        print('Вызван абстрактный метод в Seafood')


class Terminal:
    menu = ['Перейти к меню', 'Просмотреть заказ', 'Отменить позицию', 'Завершить работу']

    #
    # def __init__(self):
    #     self.order = []
    #
    @classmethod
    def show_menu_products(cls):
        try:
            products = session.query(Products).all()
            print('----------------')
            for product in products:
                print(f'{product.product_id}. {product.product_name}')
            print('----------------')
        # except:
        #     print('Ошибка бд')
        finally:
            session.commit()

    @classmethod
    def show_sauces(cls):
        try:
            session = db_connect.session_db()
            sauces = session.query(Sauces).all()
            print('----------------')
            for sauce in sauces:
                print(sauce.sauces_id, sauce.sauce_name)
            print('----------------')
        except:
            print('Ошибка бд')
        finally:
            session.commit()


    @classmethod
    def show_fillings(cls):
        try:
            session = db_connect.session_db()
            fillings = session.query(Fillings).all()
            print('----------------')
            for filling in fillings:
                print(filling.fillings_id, filling.fillings_name)
            print('----------------')
        except:
            print('Ошибка бд')
        finally:
            session.commit()


    @classmethod
    def show_dough(cls):
        try:
            session = db_connect.session_db()
            doughs = session.query(Dough).all()
            print('----------------')
            for dough in doughs:
                print(dough.dough_id, dough.dough_name)
            print('----------------')
        except:
            print('Ошибка бд')
        finally:
            session.commit()


    #
    # def make_order(self, product, choose_pizza=False):
    #     try:
    #
    #         session = db_connect.session_db()
    #
    #         # Проверяем, является ли объект product прикрепленным к текущей сессии
    #         if not session.object_session(product):
    #             product = session.merge(product)  # Привязываем объект к текущей сессии
    #
    #         new_order = Orders(time_updated=datetime.now(), client_id=3, product_type=choose_pizza)
    #         session.add(new_order)
    #         print('Ваш номер заказа:', session.query(Orders.order_id).all()[-1][0])
    #
    #     # except:
    #     #     print('Ошибка бд')
    #     finally:
    #         session.commit()
    #         session.close()
    def create_order(self, session, client_id, product_ids):
        new_order = Orders(client_id=client_id)

        for product_id in product_ids:
            product = session.query(Products).filter_by(product_id=product_id).first()
            if product:
                new_order.products.append(product)


        session.add(new_order)
        session.commit()

        return new_order

    @classmethod
    def show_order(cls, order_id):
        try:

            session = db_connect.session_db()
            order = session.query(Orders).filter(Orders.order_id == order_id).first()

            print(order.product_type)
        # except:
        #         print('Ошибка бд')
        finally:
            session.commit()


    #
    # def cancel_position(self):
    #     print('Выберите номер позиции для удаления: ')
    #     ans = int(input('>>> '))
    #     delete = self.order.pop(ans-1)
    #     print(f'Позиция {delete.name} удалена')
    @staticmethod
    def add_product_class():
        session.query(Products).filter(Products.product_id == 1).update({Products.product_obj: Pepperoni()})
        session.query(Products).filter(Products.product_id == 2).update({Products.product_obj: Seafood()})
        session.query(Products).filter(Products.product_id == 3).update({Products.product_obj: BBQ_Pizza()})
        session.commit()

    @staticmethod
    def change_compound(product_id):
        try:
            choose_pizza = session.query(Products).filter(Products.product_id == product_id).first()
            print('Хотите изменить состав пиццы?(+/-)')
            compound_ans = input('>>> ')
            new_product_obj = choose_pizza.product_obj
            if compound_ans == '-':
                pass
            elif compound_ans == '+':
                print('Стандартная добавка: ')
                print(f"Тесто: {new_product_obj.dough}")
                print(f"Соус: {new_product_obj.sauce}")
                print(f"Добавка: {new_product_obj.filling}")
                print('Что хотите поменять?(соус, тесто, добавка)')
                ans_change_compound = input('>>> ')
                if ans_change_compound == 'соус':
                    print('Доступные соусы: ')
                    Terminal.show_sauces()
                    new_sauce = input('>>> ')
                    new_product_obj.sauce = new_sauce
                elif ans_change_compound == 'тесто':
                    print('Доступное тесто: ')
                    Terminal.show_dough()
                    new_dough = input('>>> ')
                    new_product_obj.dough = new_dough
                elif ans_change_compound == 'добавка':
                    print('Доступные добавки: ')
                    Terminal.show_fillings()
                    new_fillings = input('>>> ')
                    new_product_obj.fillings = new_fillings
                else:
                    raise Exceptions.ValueError("""Ошибка ввода""")
                print('--------------------')
                print('Измененная добавка: ')
                print(f"Тесто: {new_product_obj.dough}")
                print(f"Соус: {new_product_obj.sauce}")
                print(f"Добавка: {new_product_obj.filling}")
                print('--------------------')
            return new_product_obj
        # except:
        #     print('Ошибка бд')
        finally:
            session.commit()


while True:
    t1 = Terminal()
    db_connect.create_db()
    session = db_connect.session_db()

    menu = Terminal.menu
    responce = -1
    new_order = Orders(client_id=1)
    session.add(new_order)
    session.commit()
    # t1.add_product_class()
    while responce != '4':
        print('Выберите действие: ')
        for i in range(len(menu)):
            print(f'{i + 1}.{menu[i]}')
        responce = input('>>> ')
        product = None

        if responce == '1':

            t1.show_menu_products()

            print('Выберите номер продукта: ')
            product_num = int(input('>>> '))
            product = session.query(Products).filter(Products.product_id == product_num).first()

            if product.category == 'Пицца':

                product_type = t1.change_compound(product.product_id)

            # elif: если любая другая категория, то product_type - объект этого класса, например вода
            #     pass
            # else: Обработка ошибки ввода
            #     pass
            if product:
                new_order.products.append(product)

                session.commit()



        elif responce == '2':
            order = int(input("Введите номер заказа: "))
            t1.show_order(order)
        elif responce == '3':
            t1.show_order()
            # t1.cancel_position()
        elif responce == '4':
            if product != None:

                print("Спасибо за заказ! Его уже начали готовить!")
                # for i in t1.order:
                #     i.make_pizza()
                print('Ваши пиццы готовы! Приятного аппетита!')
            else:
                pass
    break
