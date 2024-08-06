from inheratence.model.Employee import Employee
from inheratence.model.Customer import Customer



employee = Employee("EmployeeFirstName", "LastName")
customer = Customer("IamCustomer", "LastName")

print("Employee data")
print(employee.pk)
print(employee.get_full_name_and_type_dict())
print(employee.get_full_name())

print("Customer data")
print(f"Customer id: {customer.pk}")
print(f"Customer full name and type: {customer.get_full_name_and_type_dict()}")
print(f"Customer full name: {customer.get_full_name()}")