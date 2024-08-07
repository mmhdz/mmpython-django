from inheratence.model.user.employee.Employee import Employee
from inheratence.model.user.customer.Customer import Customer
from inheratence.model.user.employee.ExternalEmployee import ExternalEmployee
from inheratence.model.user.employee.PartTimeEmployee import PartTimeEmployee
from inheratence.model.SalarySystem import SalarySystem
from inheratence.model.employeeoccupation.Manager import Manager
from inheratence.model.user.customer.EnterpriseCustomer import EnterpriseCustomer
from inheratence.model.employeeoccupation.Developer import Developer
from inheratence.model.ManagementSystem import ManagementSystem

employee = Employee("EmployeeFirstName", "LastName")
external_employee = ExternalEmployee("IamExternalEmployee", "LastName")
part_time_employee = PartTimeEmployee("IamPartTimeEmployee", "LastName")

customer = Customer("IamCustomer", "LastName")
enterprise_customer = EnterpriseCustomer("EnterpriseCustomer", "LastName")


manager = Manager(employee.first_name, employee.last_name, enterprise_customer, 40)
developer = Developer(external_employee.first_name, external_employee.last_name, enterprise_customer, 48)
developer_part_time = Developer(part_time_employee.first_name, part_time_employee.last_name, customer, 30)

users_list = [employee, customer, external_employee, part_time_employee]
user_salary_list = [manager, developer, developer_part_time]

management_system = ManagementSystem()
management_system.print_user_data(users_list)

salary_system = SalarySystem()
salary_system.calculate_employee_salary(user_salary_list)
