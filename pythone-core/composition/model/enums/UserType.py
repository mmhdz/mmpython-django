from enum import Enum


class UserType(Enum):
    CUSTOMER = 1,
    Employee = 2,
    ExternalCustomer = 3,
    PartTimeEmployee = 4,
    Admin = 5
