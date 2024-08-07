class SalarySystem:

    def calculate_employee_salary(self, employees: list):
        print("Calculating salary")
        print("==================")

        for employee in employees:
            print(f"""Employee with id: {employee.pk} \n
            Salary is {employee.get_salary()}""")

