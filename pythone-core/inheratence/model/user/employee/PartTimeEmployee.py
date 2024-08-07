from inheratence.model.user.employee.Employee import Employee
from inheratence.model.enums.UserType import UserType

class PartTimeEmployee(Employee):
    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = UserType.PartTimeEmployee

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}