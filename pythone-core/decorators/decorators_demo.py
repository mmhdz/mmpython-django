import functools
import random

from decorators.model.Car import CarType


def reverse_list(function):
    @functools.wraps(function)
    def wrapper():
        func = function()
        func.reverse()
        print(func)

    return wrapper


def reverse_list_and_returns_it(function):
    @functools.wraps(function)
    def wrapper():
        func = function()
        func.reverse()
        return func

    return wrapper


def format_fist_names_as_dict_and_print(function):
    @functools.wraps(function)
    def wrapper(arg1):
        func = function(arg1)
        first_name_upper = func.upper()
        print({'First Name Upper': first_name_upper, "First name default:": func})
    return wrapper


def get_element_by_index(index: int):
    def decorator(function):
        @functools.wraps(function)
        def wrapper():
            func = function()
            element = func[index]
            print(element)
        return wrapper

    return decorator


def change_sport_car_price(function):
    @functools.wraps(function)
    def wrapper(args):
        cars = function(args)
        for car in cars:
            if car.type == CarType.SPORT_CAR:
                max_new_price = car.price + 5000.00
                new_price = random.uniform(car.price, max_new_price)
                car.change_price(f"{new_price:.2f}")

            car.print_brand()
            car.print_car_type()
            car.print_price()

    return wrapper


def filter_sport_cars(function):
    @functools.wraps(function)
    def wrapper(args):
        func = function(args)
        return [x for x in func if x.type is not CarType.FAMILY_CAR]

    return wrapper


