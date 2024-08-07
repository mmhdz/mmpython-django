class ManagementSystem:

    def print_user_data(self, users: list):
        print("User data")
        print("=========")

        for user in users:
            print(f"User with id: {user.pk} and name {user.get_full_name()}")
            print(f"Full user info {user.get_full_name_and_type_dict()}")
            print("")