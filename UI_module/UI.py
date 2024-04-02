class UI:
            
    def __init__(self, controller):
        self.controller = controller
        self.extractor_options = {
            "HPCP": "1",
            "CREMA": "2"
        }
    
    def display_menu(self):
        print("Options:")
        print("Q. Execute Qmax")
        print("Q*. Execute Qmax*")
        print("EF. Execute EarlyFusion")
        print("LF. Execute LateFusion")
        print("C. Create dataset from local machine")
        print("L. Load dataset from local machine")
        print("S. Save dataset to local machine")
        print("CM. Create dataset from MongoDB")
        print("LM. Load dataset from MongoDB")
        print("SM. Save dataset to MongoDB")
        print("L. List datasets available")
        print("E. Edit dataset")
        print("X. Exit")

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
        print()
        user_input = input("Enter your choice: ")
        
        if user_input == "C":
            print()
            list_original_songs = input("Enter list of original songs: ")
            print("Choose a feature extractor type:")
            for option, number in self.extractor_options.items():
                print(f"{number}. {option}")
            user_choice = input("Enter your choice: ")
            feature_extractor_type = next((key for key, value in self.extractor_options.items() if value == user_choice), None)
            print(feature_extractor_type)
            dataset_name = input("Enter the name of the dataset: ")
            self.controller.create_dataset(list_original_songs, feature_extractor_type, dataset_name)
        elif user_input == "S":
            self.controller.save_all_datasets()
        elif user_input == "L":
            self.controller.display_datasets()
        else:
            self.display_error("Invalid option. Please choose a valid option.")
        return False  # Continue running
