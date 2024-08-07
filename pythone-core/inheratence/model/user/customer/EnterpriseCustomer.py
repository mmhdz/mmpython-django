from inheratence.model.user.customer.Customer import Customer
from inheratence.model.enums.CustomerType import CustomerType
class EnterpriseCustomer(Customer):


    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = CustomerType.Enterprise