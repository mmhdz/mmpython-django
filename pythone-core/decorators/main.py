from decorators.decorators_demo import *
from decorators.model.Car import *

first_names_list = ["Adam", "Ian", "Django", "Flask"]
non_reversed_names_list = ["Adam", "Ian", "Django", "Flask"]

sport_car = Car("Honda", CarType.SPORT_CAR, 10500.00)
family_car = Car("Peugeot", CarType.FAMILY_CAR, 7500.00)
cars = [sport_car, family_car]


@format_fist_names_as_dict_and_print
def filter_first_name_by_index(index: int):
    return first_names_list[index]


@reverse_list
def get_first_name_list_reversed():
    return first_names_list


@get_element_by_index(0)
@reverse_list_and_returns_it
def multiple_decorators():
    return non_reversed_names_list


@change_sport_car_price
@filter_sport_cars
def change_car_info_and_print_it(cars_list: list):
    return cars_list


if __name__ == "__main__":
    filter_first_name_by_index(2)
    get_first_name_list_reversed()
    multiple_decorators()
    change_car_info_and_print_it(cars)

