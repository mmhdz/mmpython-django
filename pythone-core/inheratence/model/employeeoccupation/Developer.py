from inheratence.model.salary.DeveloperSalary import DeveloperSalary
from inheratence.model.user.employee.Employee import Employee
from inheratence.model.enums.EmployeeOccupancy import EmployeeOccupancy
from inheratence.model.user.customer.Customer import Customer
from inheratence.util.GeneralUtil import GeneralUtil


class Developer(Employee, DeveloperSalary):

    def __init__(self, first_name: str, last_name: str, client: Customer, working_hours: int):
        overtime = GeneralUtil.calculate_overtime(working_hours)
        super().__init__(first_name, last_name)
        DeveloperSalary.__init__(self, working_hours, 7.80, overtime)
        self.client = client
        self.occupancy = EmployeeOccupancy.Manager

    def get_salary(self):
        return super().calculate_salary()
