import uuid

from composition.model.Salary import Salary
from composition.model.enums.CustomerType import CustomerType
from inheratence.model.enums.UserType import UserType
from inheratence.model.enums.EmployeeOccupancy import EmployeeOccupancy

class User:
    def __init__(self, first_name: str, last_name: str):
        self.pk = uuid.uuid1()
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Employee(User):
    def __init__(self, first_name: str, last_name: str, salary: Salary):
        super().__init__(first_name, last_name)
        self.type = UserType.Employee
        self.salary = salary

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}

    def get_salary(self):
        return self.salary.calculate_salary()


class PartTimeEmployee(Employee):
    def __init__(self, first_name: str, last_name: str, salary: Salary):
        super().__init__(first_name, last_name, salary)
        self.type = UserType.PartTimeEmployee

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}

    def get_salary(self):
        return super().salary.calculate_salary()


class ExternalEmployee:

    def __init__(self, first_name: str, last_name: str, salary: Salary):
        self.pk = uuid.uuid1()
        self.first_name = first_name
        self.last_name = last_name
        self.type = UserType.ExternalCustomer
        self.salary = salary

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': self.get_full_name(), 'user_type': self.type.name}

    def get_salary(self):
        return self.salary.calculate_salary()


class Customer(User):
    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = UserType.CUSTOMER

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}


class EnterpriseCustomer(Customer):

    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = CustomerType.Enterprise

    def get_full_name_and_type_dict(self) -> dict:
        return super().get_full_name_and_type_dict()


class Developer(Employee):

    def __init__(self, first_name: str, last_name: str, client: Customer, salary: Salary):
        super().__init__(first_name, last_name, salary)
        self.client = client
        self.occupancy = EmployeeOccupancy.Developer

    def get_salary(self):
        return super().get_salary()


class Manager(Employee):
    def __init__(self, first_name: str, last_name: str, client: Customer, salary: Salary):
        super().__init__(first_name, last_name, salary)
        self.salary = salary
        self.client = client
        self.occupancy = EmployeeOccupancy.Manager

    def get_salary(self):
        return super().get_salary()