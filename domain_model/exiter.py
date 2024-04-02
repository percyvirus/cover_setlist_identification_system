# exiter.py

class Exiter:
    def __init__(self, ui):
        self.ui = ui

    def exit_spreadsheet(self):
        response = self.ui.get_user_input("Do you want to exit without saving? (Y/N): ")
        if response.lower() == "y":
            print("\nExiting spreadsheet...\n")
            # Additional logic for handling spreadsheet exiting
        elif response.lower() == "n":
            print("\nContinuing...\n")
        else:
            print("\nInvalid option. Please enter 'Y' or 'N'.\n")
            self.exit_spreadsheet()
