import uuid

from inheratence.model.User import User
from inheratence.model.enums.UserType import UserType


class Employee(User):
    def __init__(self, first_name: str, last_name: str):
        super().__init__(first_name, last_name)
        self.type = UserType.Employee

    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': super().get_full_name(), 'user_type': self.type.name}
