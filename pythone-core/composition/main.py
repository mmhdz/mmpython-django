from composition.model.User import *
from composition.model.Salary import *
from composition.model.ManagementSystem import *
from composition.model.SalarySystem import *


enterprise_customer = EnterpriseCustomer("EnterpriseCustomer", "LastName")
developer_salary = DeveloperSalary(working_hours=40, hourly_rate=11.5, project_overtime=10)
manager_salary = ManagerSalary(working_hours=40, hourly_rate=20.5)


developer = Developer("DeveloperFirstName", "LastName", enterprise_customer, developer_salary)
manager = Manager("ManagerFirstName", "LastName", enterprise_customer, manager_salary)

employee_list = [developer, manager]


management_system = ManagementSystem()
management_system.print_user_data(employee_list)

salary_system = SalarySystem()
salary_system.calculate_employee_salary(employee_list)

