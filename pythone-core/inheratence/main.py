from inheratence.model.SalarySystem import SalarySystem
from inheratence.model.ManagementSystem import ManagementSystem
from inheratence.model.User import *



customer = Customer("IamCustomer", "LastName")


manager = Manager("MangerFirstName", "LastName", customer, 40)
developer = Developer("DeveloperFirstName", "LastName", customer, 48)

employees = [manager, developer]

management_system = ManagementSystem()
management_system.print_user_data(employees)

salary_system = SalarySystem()
salary_system.calculate_employee_salary(employees)
