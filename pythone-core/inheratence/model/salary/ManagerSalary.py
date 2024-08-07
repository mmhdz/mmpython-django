from inheratence.model.salary.Salary import Salary


class ManagerSalary(Salary):

    def __init__(self, working_hours: int, hourly_rate: float):
        self.working_hours = working_hours
        self.rate = hourly_rate
        super().__init__(self.calculate_salary())

    def calculate_salary(self):
        return self.working_hours * self.rate

