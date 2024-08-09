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


@change_sport_cars_price
@filter_sport_cars
def change_car_info_and_print_it(cars_list: list):
    return cars_list


@general_purpose_decorator
def function_with_no_args():
    print("No arguments")


@general_purpose_decorator
def function_with_args(name: str, number: int, cars_list: list):
    print(f"Name is {name}, number is {number}, cars types are {[x.type.name for x in cars_list]}")


@general_purpose_decorator
def function_with_keywords(name: str, number: int):
    print(f"Name is {name}, number is {number}")


@get_element_by_index_with_func_parameters(cars, CarType.SPORT_CAR)
def get_number_of_cars_by_type(cars_list: list, car_type: CarType):
    print(f"Number of cars with type {car_type.name} in the list are {len([x for x in cars_list if x.type == car_type])}")


if __name__ == "__main__":
    filter_first_name_by_index(2)
    get_first_name_list_reversed()
    multiple_decorators()
    change_car_info_and_print_it(cars)
    function_with_no_args()
    function_with_args(sport_car.brand, 1402, cars)
    function_with_keywords(name=family_car.brand, number=101)
    get_number_of_cars_by_type(cars, CarType.FAMILY_CAR)
