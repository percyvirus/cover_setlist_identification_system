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

def contar_canciones_originales_en_subdirectorios(directorio_principal):
    subdirectorios = [d for d in os.listdir(directorio_principal) if os.path.isdir(os.path.join(directorio_principal, d)) and d.startswith('W_')]
    count = 1
    count_bis = 0
    for subdirectorio in subdirectorios:
        print(f"Analizando subdirectorio ({count}): {subdirectorio}")
        directorio_actual = os.path.join(directorio_principal, subdirectorio)
        archivos_h5 = buscar_archivos_h5(directorio_actual)
        canciones_originales = buscar_originales_en_archivos_h5(archivos_h5)
        print(f"Cantidad de canciones originales encontradas en {subdirectorio}: {len(canciones_originales)}")
        if len(canciones_originales) != 1:
            print("Aquí hay un numero diferente a 1 de works")
        count_bis = count_bis + len(canciones_originales)
        count = count +1
    print(f"En total hay {count_bis} works")
    
def contar_canciones_covers_en_subdirectorios(directorio_principal):
    subdirectorios = [d for d in os.listdir(directorio_principal) if os.path.isdir(os.path.join(directorio_principal, d)) and d.startswith('W_')]
    count = 1
    count_bis = 0
    for subdirectorio in subdirectorios:
        print(f"Analizando subdirectorio ({count}): {subdirectorio}")
        directorio_actual = os.path.join(directorio_principal, subdirectorio)
        archivos_h5 = buscar_archivos_h5(directorio_actual)
        canciones_covers = buscar_covers_en_archivos_h5(archivos_h5)
        print(f"Cantidad de canciones originales encontradas en {subdirectorio}: {len(canciones_covers)}")
        if len(canciones_covers) != 1:
            print("Aquí hay un numero diferente a 1 de cover")
        count_bis = count_bis + len(canciones_covers)
        count = count +1
    print(f"En total hay {count_bis} covers")

def buscar_originales_en_archivos_h5(archivos_h5):
    originales = []
    for archivo in archivos_h5:
        file = dd.io.load(archivo)
        if file['second_hand_song_API_features']['is_original'][()]:
            originales.append(archivo)
    return originales

def buscar_covers_en_archivos_h5(archivos_h5):
    covers = []
    for archivo in archivos_h5:
        file = dd.io.load(archivo)
        if not file['second_hand_song_API_features']['is_original'][()]:
            covers.append(archivo)
    return covers

# Directorio donde buscar archivos .h5
directorio_principal = "/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended"
contar_canciones_originales_en_subdirectorios(directorio_principal)
contar_canciones_covers_en_subdirectorios(directorio_principal)