import os
import h5py
import deepdish as dd

def buscar_archivos_h5(directorio):
    archivos_h5 = []
    for root, dirs, files in os.walk(directorio):
        for file in files:
            if file.endswith('.h5'):
                archivos_h5.append(os.path.join(root, file))
    return archivos_h5

def buscar_originales_en_archivos_h5(archivos_h5):
    originales = []
    for archivo in archivos_h5:
        file = dd.io.load(archivo)
        if file['second_hand_song_API_features']['is_original'][()]:
            originales.append(archivo)
    return originales

# Directorio donde buscar archivos .h5
directorio_principal = "/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended"

# Buscar archivos .h5 en el directorio principal y subdirectorios
archivos_h5 = buscar_archivos_h5(directorio_principal)

# Buscar canciones originales en los archivos .h5 encontrados
canciones_originales = buscar_originales_en_archivos_h5(archivos_h5)

# Imprimir los archivos .h5 que contienen canciones originales
for cancion_original in canciones_originales:
    print(f"Canción original encontrada en el archivo .h5: {cancion_original}")
