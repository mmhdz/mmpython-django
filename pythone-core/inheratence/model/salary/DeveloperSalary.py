from inheratence.model.salary.Salary import Salary


class DeveloperSalary(Salary):

    def __init__(self, working_hours: int, hourly_rate: float, project_overtime: float):
        self.working_hours = working_hours
        self.rate = hourly_rate
        self.project_overtime = project_overtime
        super().__init__(self.calculate_salary())

    def calculate_salary(self):
        return self.working_hours * self.rate + self.project_overtime * 14.5
