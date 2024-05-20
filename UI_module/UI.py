class UI:
            
    def __init__(self, controller, datasets):
        self.controller = controller
        self.datasets = datasets
        self.extractor_options = {
            "1": "HPCP",
            "2": "CREMA"
        }
        self.menu_options = {
            "1": "Load dataset from local machine",
            "2": "Load dataset from MongoDB",
            "3": "Create dataset from local machine",
            "4": "Save dataset to local machine",
            "5": "Save dataset to MongoDB",
            "6": "List loaded datasets",
            "7": "Edit dataset",
            "8": "Execute Qmax",
            "9": "Execute Qmax*",
            "10": "Execute EarlyFusion",
            "11": "Execute LateFusion",
            "12": "Get Statistics",
            "13": "Exit",
            "14": "Execute Qmax* with COVERS80"
        }
        self.user_choices = {
        }
    
    def display_menu(self):
        print("\nMenu:")
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
        print(f"\n{output_message}")

    def handle_user_input(self):
        self.user_choices = {
        }
        user_input = self.get_user_input("Enter your choice: ")
        self.user_choices[len(self.user_choices)] = f"  - Menu option: ({user_input}. {self.menu_options[user_input]})"
        
        if self.menu_options[user_input] == "Load dataset from local machine":  #DONE
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
                
            dataset_path = self.get_user_input("Enter dataset path: ")
            self.user_choices[len(self.user_choices)] = f"  - Dataset path: ({dataset_path})"
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            self.controller.load_datasets(dataset_path)
            print()
            print("Press enter to continue...")
            input()  # Wait for the user to press Enter
        elif self.menu_options[user_input] == "Load dataset from MongoDB":  #TODO
            print()
        elif self.menu_options[user_input] == "Create dataset from local machine":  #DONE
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            
            self.display_message("Choose a feature extractor type:")
            for number, option in self.extractor_options.items():
                print(f"{number}. {option}")
            user_input = self.get_user_input("Enter your choice: ")
            
            self.user_choices[len(self.user_choices)] = f"  - Feature extractor type: ({user_input}. {self.extractor_options[user_input]})"
            
            feature_extractor_type = self.extractor_options[user_input]
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            
            list_original_songs = self.get_user_input("Enter list of original songs: ")
            self.user_choices[len(self.user_choices)] = f"  - List of original songs: ({list_original_songs})"
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
                
            dataset_name = self.get_user_input("Enter dataset name: ")
            self.user_choices[len(self.user_choices)] = f"  - Dataset name: ({dataset_name})"
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
                
            self.controller.create_dataset(list_original_songs, feature_extractor_type, dataset_name)
        elif self.menu_options[user_input] == "Save dataset to local machine":
            self.controller.save_all_datasets()
        elif self.menu_options[user_input] == "Save dataset to MongoDB":
            print()
        elif self.menu_options[user_input] == "List loaded datasets":
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            self.controller.display_datasets()
            print("Press enter to continue...")
            input()  # Wait for the user to press Enter
        elif self.menu_options[user_input] == "Edit dataset":
            print()
        elif self.menu_options[user_input] == "Execute Qmax":
            keys = list(self.datasets.keys())
            self.datasets_options = {str(i+1): clave for i, clave in enumerate(keys)}
            self.display_message("Choose number of dataset to be used:")
            for number, option in self.datasets_options.items():
                print(f"{number}. {option}")
            user_input = self.get_user_input("Enter your choice: ")
            dataset_name = self.datasets_options[user_input]
            dataset = self.datasets[dataset_name]
            results_path = self.get_user_input("Enter path where to save results: ")
            self.user_choices[len(self.user_choices)] = f"  - Results path: ({results_path})"
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            print()
            print("Press enter to continue...")
            self.controller.execute_qmax(dataset, results_path)
        elif self.menu_options[user_input] == "Execute Qmax*":
            keys = list(self.datasets.keys())
            self.datasets_options = {str(i+1): clave for i, clave in enumerate(keys)}
            self.display_message("Choose number of dataset to be used:")
            for number, option in self.datasets_options.items():
                print(f"{number}. {option}")
            user_input = self.get_user_input("Enter your choice: ")
            
            dataset_name = self.datasets_options[user_input]
            dataset = self.datasets[dataset_name]
            
            results_path = self.get_user_input("Enter path where to save results: ")
            self.user_choices[len(self.user_choices)] = f"  - Results path: ({results_path})"
            
            self.display_message("User choises/inputs:")
            for number, choice in self.user_choices.items():
                print(choice)
            print()
            print("Press enter to continue...")
            self.controller.execute_qmax_bis(dataset, results_path)
        elif self.menu_options[user_input] == "Execute EarlyFusion":
            print()
        elif self.menu_options[user_input] == "Execute LateFusion":
            print()
        elif self.menu_options[user_input] == "Get Statistics":
            confusion_matrix_path = input("Enter confusion matrix path: ")
            self.controller.get_statistics(confusion_matrix_path)
        elif self.menu_options[user_input] == "Exit":
            self.controller.exit_program()
        elif self.menu_options[user_input] == "Execute Qmax* with COVERS80":
            self.controller.execute_Qmax_bis_with_COVERS80()
        else:
            self.display_error("Invalid option. Please choose a valid option.")
        return False  # Continue running
