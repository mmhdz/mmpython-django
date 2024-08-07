class SalarySystem:

    def calculate_employee_salary(self, employees: list):
        print("Calculating salary")
        print("==================")

        for employee in employees:
            print(f"Employee with id: {employee.pk}")
            print(f"Salary is {employee.get_salary(): .2f}")
            print(f"And work for {employee.get_work_hrs()}")
            print("======================================")

