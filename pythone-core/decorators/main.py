from decorators.decorators_demo import *

first_names_list = ["Adam", "Ian", "Django", "Flask"]
non_reversed_names_list = ["Adam", "Ian", "Django", "Flask"]


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


if __name__ == "__main__":
    filter_first_name_by_index(2)
    get_first_name_list_reversed()
    multiple_decorators()

