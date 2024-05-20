import deepdish as dd

file_path_1 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/LODI_1/W_20905/P_20916.h5'
propio_1 = dd.io.load(file_path_1)

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