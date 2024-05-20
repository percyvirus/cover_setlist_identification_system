import os
import deepdish as dd
from domain_model.dataset import Dataset

class DatasetLoader:
    def __init__(self, controller):
        self.controller = controller
        self.dataset = Dataset()    #TODO: ¿Cómo hago para utilizar Dataset() directamente de controller? o simplemente cambiar "datasets" por "database"
        
    def load_dataset_locally(self, folder_path, save_locally=True, save_to_mongodb=True):
        #spreadsheet = ISpreadsheetControllerForChecker()
        folder_name = os.path.basename(folder_path)
        try:
            all_items = os.listdir(folder_path)
            subfolders = [item for item in all_items if item.startswith('W_') and os.path.isdir(os.path.join(folder_path, item))]
            for subfolder in subfolders:
                original_song_folder = os.path.join(folder_path, subfolder)
                for _, _, song_files in os.walk(original_song_folder):
                    song_files = [item for item in song_files if item.endswith('.h5')] # To avoid '.DS_Store'
                    for song_file in song_files:
                        song_data = dd.io.load(os.path.join(original_song_folder, song_file))
                        if song_data["track_id"] == 'P_performance_ID_not_found':
                            self.dataset.add_data(song_data["track_id"] + '_' + song_data["label"], song_data)
                        else:
                            self.dataset.add_data(song_data["track_id"], song_data)
            self.controller.datasets[folder_name] = self.dataset
            print(f"\nDataset {folder_name} loaded")
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except IOError:
            print("Error opening the file.")
        except Exception as e:
            self.ui.display_error(f"Error loading dataset from h5 file: {str(e)}")
            return None
    

