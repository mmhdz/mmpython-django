from inheratence.model.Employee import Employee
from inheratence.model.Customer import Customer
from inheratence.model.ExternalCustomer import ExternalCustomer
from inheratence.model.ManagementSystem import ManagementSystem


employee = Employee("EmployeeFirstName", "LastName")
customer = Customer("IamCustomer", "LastName")
external_customer = ExternalCustomer("IamExternalCustomer", "LastName")

users_list = [employee, customer, external_customer]

management_system = ManagementSystem()
management_system.print_user_data(users_list)