class UI:
            
    def __init__(self, controller):
        self.controller = controller
        self.extractor_options = {
            "1": "HPCP",
            "2": "CREMA"
        }
        self.menu_options = {
            "1": "Execute Qmax",
            "2": "Execute Qmax*",
            "3": "Execute EarlyFusion",
            "4": "Execute LateFusion",
            "5": "Create dataset from local machine",
            "6": "Load dataset from local machine",
            "7": "Save dataset to local machine",
            "8": "Load dataset from MongoDB",
            "9": "Save dataset to MongoDB",
            "10": "List datasets available",
            "11": "Edit dataset",
            "12": "Exit"
        }
        self.user_choices = {
        }
    
    def display_menu(self):
        print("Menu:")
        for number, option in self.menu_options.items():
                print(f"{number}. {option}")

    def wait_for_enter(self):
        print("Press enter to continue...")
        input()  # Wait for the user to press Enter

    def get_user_input(self, message):
        return input(f"\n{message}")

    def display_error(self, error_message):
        print(f"\nError: {error_message}\n")
        
    def display_message(self, output_message):
        print(f"\n{output_message}\n")

    def handle_user_input(self):
        self.user_choices = {
        }
        print()
        user_input = input("Enter your choice: ")
        print()
        self.user_choices[len(self.user_choices)] = f"  - Menu option: ({user_input}. {self.menu_options[user_input]})"
        
        if self.menu_options[user_input] == "Execute Qmax":
            print()
        elif self.menu_options[user_input] == "Execute Qmax*":
            print()
        elif self.menu_options[user_input] == "Execute EarlyFusion":
            print()
        elif self.menu_options[user_input] == "Execute LateFusion":
            print()
        elif self.menu_options[user_input] == "Create dataset from local machine":
            print("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            print()
            
            print("Choose a feature extractor type:")
            for number, option in self.extractor_options.items():
                print(f"{number}. {option}")
            print()
            user_input = input("Enter your choice: ")
            print()
            
            self.user_choices[len(self.user_choices)] = f"  - Feature extractor type: ({user_input}. {self.extractor_options[user_input]})"
            
            feature_extractor_type = self.extractor_options[user_input]
            print("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            print()
            
            list_original_songs = input("Enter list of original songs: ")
            print()
            self.user_choices[len(self.user_choices)] = f"  - List of original songs: ({list_original_songs})"
            print("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            print()
            dataset_name = input("Enter dataset name: ")
            print()
            self.user_choices[len(self.user_choices)] = f"  - Dataset name: ({dataset_name})"
            print("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            self.controller.create_dataset(list_original_songs, feature_extractor_type, dataset_name)
        elif self.menu_options[user_input] == "Load dataset from local machine":
            print()
        elif self.menu_options[user_input] == "Save dataset to local machine":
            self.controller.save_all_datasets()
        elif self.menu_options[user_input] == "Load dataset from MongoDB":
            print()
        elif self.menu_options[user_input] == "Save dataset to MongoDB":
            print()
        elif self.menu_options[user_input] == "List datasets available":
            self.controller.display_datasets()
        elif self.menu_options[user_input] == "Edit dataset":
            print()
        elif self.menu_options[user_input] == "Exit":
            self.controller.exit_program()
        else:
            self.display_error("Invalid option. Please choose a valid option.")
        return False  # Continue running
