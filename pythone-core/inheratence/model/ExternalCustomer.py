import uuid
from inheratence.model.enums.UserType import UserType

class ExternalCustomer:


    def __init__(self, first_name: str, last_name: str):
        self.pk = uuid.uuid1()
        self.first_name = first_name
        self.last_name = last_name
        self.type = UserType.ExternalCustomer
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


    def get_full_name_and_type_dict(self) -> dict:
        return {'full_name': self.get_full_name(), 'user_type': self.type.name}