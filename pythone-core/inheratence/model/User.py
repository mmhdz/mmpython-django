import uuid

from composition.model.User import Customer
from inheratence.model.enums.EmployeeOccupancy import EmployeeOccupancy
from inheratence.model.enums.UserType import UserType
from inheratence.util.GeneralUtil import GeneralUtil


class User:
    def __init__(self, first_name: str, last_name: str):
        self.pk = uuid.uuid1()
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Employee(User):
    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = UserType.Employee

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}

    def get_salary(self):
        pass

    def get_work_hrs(self):
        pass

class PartTimeEmployee(Employee):
    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = UserType.PartTimeEmployee

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}

class ExternalEmployee:

    def __init__(self, first_name: str, last_name: str):
        self.pk = uuid.uuid1()
        self.first_name = first_name
        self.last_name = last_name
        self.type = UserType.ExternalCustomer

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': self.get_full_name(), 'user_type': self.type.name}


class DeveloperSalary(Employee):

    def __init__(self, first_name: str, last_name: str, working_hours: int, hourly_rate: float, project_overtime: float):
        super().__init__(first_name, last_name)
        self.working_hours = working_hours
        self.rate = hourly_rate
        self.project_overtime = project_overtime

    def calculate_salary(self):
        return self.working_hours * self.rate + self.project_overtime * 14.5

    def work(self):
        print(f"Developer work {self.working_hours + self.project_overtime} hrs this week.")


class ManagerSalary(Employee):

    def __init__(self, first_name: str, last_name: str, working_hours: int, hourly_rate: float):
        super().__init__(first_name, last_name)
        self.working_hours = working_hours
        self.rate = hourly_rate

    def calculate_salary(self):
        return self.working_hours * self.rate
    
    def work(self):
        print(f"Manager work {self.working_hours} hrs  this week.")


class Developer(DeveloperSalary):

    def __init__(self, first_name: str, last_name: str, client: Customer, working_hours: int):
        overtime = GeneralUtil.calculate_overtime(working_hours)
        super().__init__(first_name, last_name, working_hours, 24.4, overtime)
        self.client = client
        self.occupancy = EmployeeOccupancy.Manager

    def get_salary(self):
        return super().calculate_salary()

    def get_work_hrs(self):
        super().work()


class Manager(ManagerSalary):
    def __init__(self, first_name: str, last_name: str, client: Customer, working_hours: int):
        super().__init__(first_name, last_name, working_hours, 32.10)
        self.client = client
        self.occupancy = EmployeeOccupancy.Manager

    def get_salary(self):
        return super().calculate_salary()

    def get_work_hrs(self):
        super().work()
        
