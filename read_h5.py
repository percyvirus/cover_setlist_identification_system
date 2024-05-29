import deepdish as dd
import numpy as np
import os

file_path_1 = './ORIGEN_dataset.h5'
propio_1 = dd.io.load(file_path_1)

def save_dataset_locally(dataset, folder_path):
    for track_id, data_dataset in dataset.iterate_data():
        work = data_dataset.get('label')
        subfolder_path = f"{folder_path}/{work}"
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)
        
        file_name = subfolder_path+f'/{track_id}.h5'
        np.object = object # Since version 1.24 of numpy, np.object is deprecated, and needs to be replaced with object 
        dd.io.save(file_name, data_dataset)

folder_path = folder_path = f"/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/ORIGEN_extended"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    save_dataset_locally(propio_1[1], folder_path)
else:
    user_choise = input(f"The dataset '{folder_path}' already exists. Do you wanna overwritte it? (Y/N)")
    if user_choise== "Y":
        save_dataset_locally(propio_1[1], folder_path)
    elif user_choise== "N":
        pass
    
for track_id, data_dataset in propio_1.iterate_data():
    work = data_dataset.get('label')
    subfolder_path = f"{folder_path}/{work}"
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    
    file_name = subfolder_path+f'/{track_id}.h5'
    np.object = object # Since version 1.24 of numpy, np.object is deprecated, and needs to be replaced with object 
    dd.io.save(file_name, data_dataset)

file_path_2 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/LODI_2/W_20905/P_20916.h5'
propio_2 = dd.io.load(file_path_2)

file_path_3 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/oli_extended/W_8963/P_138253.h5'
propio_3 = dd.io.load(file_path_3)

print("original_performances_that_are_not_original_performance_list:")
for elemento in propio_1.get('original_performances_that_are_not_original_performance_list'):
    print(elemento)

print("cover_performances_that_are_not_cover_performance_list:")
for elemento in propio_1.get('cover_performances_that_are_not_cover_performance_list'):
    print(elemento)

print(propio_1)