import json
import csv

def comparar_results_csv(results1_path, results2_path, output_csv_path):
    # Cargar los archivos JSON
    with open(results1_path, 'r') as file:
        results1 = json.load(file)
    with open(results2_path, 'r') as file:
        results2 = json.load(file)
    
    # Obtener los rankings de ambos archivos
    rankings1 = results1["Rankings"]
    rankings2 = results2["Rankings"]
    
    with open(output_csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Key", "Position1", "Distance1", "Position2", "Distance2"])
        
        # Iterar sobre las claves de los rankings y comparar las posiciones
        for key in rankings1.keys():
            if key in rankings2:  # Comprobar si la clave está presente en ambos resultados
                position1 = rankings1[key]["position"]
                distance1 = rankings1[key]["distance"]
                position2 = rankings2[key]["position"]
                distance2 = rankings2[key]["distance"]
                if position1 > 1 or position2 > 1:
                    writer.writerow([key, position1, distance1, position2, distance2])
            else:
                # Si la clave no está presente en uno de los resultados, imprimir un mensaje de advertencia
                print(f"La clave {key} no está presente en ambos resultados.")

# Rutas de los archivos results.json
results1_path = "/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/COVERS80_extended/RESULTS/Qmax_bis_12_bins_1_results.json"
results2_path = "/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended/RESULTS/Qmax_bis_12_bins_results.json"
output_csv_path = "comparacion_results.csv"

comparar_results_csv(results1_path, results2_path, output_csv_path)

print("Se ha creado el archivo CSV de comparación de resultados:", output_csv_path)
