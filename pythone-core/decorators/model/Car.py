from enum import Enum


class CarType(Enum):
    SPORT_CAR = 1,
    FAMILY_CAR = 2,
    SEDAN = 3


class Car:

    def __init__(self, brand: str, type: CarType, price: float):
        self.brand = brand
        self.type = type
        self.price = price

    def change_price(self, new_price: float):
        self.price = new_price

    def print_brand(self):
        print(self.brand)

    def print_car_type(self):
        print(self.type.name)

    def print_price(self):
        print(self.price)



