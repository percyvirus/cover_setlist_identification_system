import os
import h5py
import numpy as np
import deepdish as dd

class DatasetSaver:
    def __init__(self, controller):
        self.controller = controller

    def save_dataset_locally(self, dataset, folder_path):
        
        for track_id, data_dataset in dataset.iterate_data():
            work = data_dataset.get('label')
            subfolder_path = f"{folder_path}/{work}"
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            
            file_name = subfolder_path+f'/{track_id}.h5'
            np.object = object # Since version 1.24 of numpy, np.object is deprecated, and needs to be replaced with object 
            dd.io.save(file_name, data_dataset)
            
        '''
        with h5py.File('/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIO/W_6536.h5', 'w') as f:
            # Guardar los datos de HPCP
            f.create_dataset('hpcp', data=query_hpcp_12_1)
            # Guardar la etiqueta y el ID de la pista
            f.attrs['label'] = label
            f.attrs['track_id'] = track_id
        '''

    def save_dataset_mongodb(self, dataset, collection_name):
        # Aquí implementar la lógica para guardar en MongoDB
        pass

    def save_dataset(self, dataset, save_locally=True, save_to_mongodb=True):
        if dataset:
            if save_locally:
                folder_path = f"/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/{dataset[0]}"
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                    self.save_dataset_locally(dataset[1], folder_path)
                else:
                    user_choise = input(f"The dataset '{folder_path}' already exists. Do you wanna overwritte it? (Y/N)")
                    if user_choise== "Y":
                        self.save_dataset_locally(dataset[1], folder_path)
                    elif user_choise== "N":
                        pass
            if save_to_mongodb:
                collection_name = f"/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/{dataset_name}_collection"
                self.save_dataset_mongodb(dataset, collection_name)
                print(f"Dataset '{dataset_name}' saved to MongoDB collection '{collection_name}'")
        else:
            print(f"Dataset '{dataset_name}' not found in the controller")

# Ejemplo de uso:
# saver = DatasetSaver(controller)
# saver.save_dataset("dataset_name", save_locally=True, save_to_mongodb=True)
