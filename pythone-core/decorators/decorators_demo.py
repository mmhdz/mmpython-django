import functools


def get_fist_name_from_index(index: int):
    def decorator(function):
        @functools.wraps(function)
        def wrapper_return_by_index():
            func = function()
            return func[index]

        return wrapper_return_by_index

    return decorator


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
