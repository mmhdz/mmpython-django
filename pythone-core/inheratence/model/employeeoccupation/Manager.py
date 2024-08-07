from inheratence.model.user.employee.Employee import Employee
from inheratence.model.enums.EmployeeOccupancy import EmployeeOccupancy
from inheratence.model.user.customer.Customer import Customer
from inheratence.model.salary.ManagerSalary import ManagerSalary


class Manager(Employee, ManagerSalary):
    def __init__(self, first_name: str, last_name: str, client: Customer, working_hours: int):
        super().__init__(first_name, last_name)
        ManagerSalary.__init__(self, working_hours, 7.80)
        self.client = client
        self.occupancy = EmployeeOccupancy.Manager

    def get_salary(self):
        return super().calculate_salary()
