
class GeneralUtil:


    @staticmethod
    def calculate_overtime(working_hrs: int):
        overtime = 0
        if working_hrs > 40:
            for i in range(working_hrs, 0, -1):
                working_hrs -= 1
                overtime += 1
                if working_hrs == 40:
                    break

        return overtime
