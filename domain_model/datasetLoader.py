import sys 
import os

sys.path.append(os.getcwd())
from domain_model import *

class DatasetLoader:

    #NOTA: La classe i sus funciones se encuentran implementadas en ISpreadsheetControllerForChecker
    # El codigo posterior está duplicado. Ver ISpreadsheetControllerForChecker

    def __init__(self):
        pass
        
    def load_spreadsheet_from_s2v_file(self, file_path):
        spreadsheet = ISpreadsheetControllerForChecker()
        formulas = {}  # To store formulas and process them later
        
        try:
            with open(file_path, "r") as s2v_file:
                for row_num, line in enumerate(s2v_file):
                    cells = line.strip().split(";")
                    for col_num, cell_content in enumerate(cells):
                        coord = chr(col_num + ord('A')) + str(row_num + 1)
                        if cell_content:
                            if cell_content.startswith("="):
                                cell_content = cell_content.replace(",", ";")
                                # If the cell_content is a formula, store it for later processing
                                formulas[coord] = cell_content
                            else:
                                spreadsheet.set_cell_content(coord, cell_content)
        except Exception as e:
            self.ui.display_error(f"Error loading spreadsheet from S2V file: {str(e)}")
            return None
        
        # Process the formulas after adding all other cells
        for coord, formula_content in formulas.items():
            spreadsheet.set_cell_content(coord, formula_content)
        
        return spreadsheet

