import deepdish as dd

file_path_1 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended_SHORT/W_26/P_26.h5'
propio_1 = dd.io.load(file_path_1)

file_path_2 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended_SHORT/W_26/P_26.h5'
propio_2 = dd.io.load(file_path_2)

file_path_3 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended/W_2835/P_64060.h5'
propio_3 = dd.io.load(file_path_3)

print("original_performances_that_are_not_original_performance_list:")
for elemento in propio_1.get('original_performances_that_are_not_original_performance_list'):
    print(elemento)

print("cover_performances_that_are_not_cover_performance_list:")
for elemento in propio_1.get('cover_performances_that_are_not_cover_performance_list'):
    print(elemento)

print(propio_1)