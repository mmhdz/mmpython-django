import uuid


class User:
    def __init__(self, first_name: str, last_name: str):
        self.pk = uuid.uuid1()
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"





