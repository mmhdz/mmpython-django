class Salary:

    def __init__(self, weekly_salary: float):
        self.weekly_salary = weekly_salary

    def calculate_salary(self):
        return self.weekly_salary


class DeveloperSalary(Salary):

    def __init__(self, working_hours: int, hourly_rate: float, project_overtime: float):
        self.working_hours = working_hours
        self.rate = hourly_rate
        self.project_overtime = project_overtime
        super().__init__(self.calculate_salary())

    def calculate_salary(self):
        return self.working_hours * self.rate + self.project_overtime * 14.5


class ManagerSalary(Salary):

    def __init__(self, working_hours: int, hourly_rate: float):
        self.working_hours = working_hours
        self.rate = hourly_rate
        super().__init__(self.calculate_salary())

    def calculate_salary(self):
        return self.working_hours * self.rate