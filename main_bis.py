import json
import deepdish as dd
import essentia.standard as estd
from essentia.pytools.spectral import hpcpgram
import h5py
import numpy as np
import matplotlib.pyplot as plt
import math

# Loading metadata files (json files)
# Benchmark metadata
with open('/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/Da-TACOS/da-tacos_metadata/da-tacos_benchmark_subset_metadata.json') as f:
	benchmark_metadata = json.load(f)
print(type(benchmark_metadata))

# Cover analysis metadata
with open('/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/Da-TACOS/da-tacos_metadata/da-tacos_coveranalysis_subset_metadata.json') as f:
	coveranalysis_metadata = json.load(f)
print(type(coveranalysis_metadata))


# Loading pre-extracted features files (h5 files)
# Benchmark features from P_7581 for W_7581
file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/Da-TACOS/da-tacos_benchmark_subset_hpcp/W_7581_hpcp/P_7581_hpcp.h5'
P_7581_data = dd.io.load(file_path)
print(type(P_7581_data))
print(type(P_7581_data['hpcp']))
print(type(P_7581_data['label']))
print(type(P_7581_data['track_id']))
print(P_7581_data)

# Benchmark features from P_86643 for W_7581
file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/Da-TACOS/da-tacos_benchmark_subset_hpcp/W_7581_hpcp/P_86643_hpcp.h5'
P_86643_data = dd.io.load(file_path)

frame_size = 16000 * 0.1
frame_size = int(2 ** math.ceil(math.log2(frame_size)))
hop_size=int(frame_size/2)

# Features extracted manually
file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/COVERS80_extended_bis/RESULTS/Qmax_bis_12_bins_1.h5'
propio_1 = dd.io.load(file_path)

file_path = f"{file_path.replace('.h5', '')}.json"
            
#with open(file_path, "w") as json_file:
    #json.dump(propio_1, json_file, indent=4)

    #print("Results saved at", file_path)
#print(type(propio_1))
print(propio_1['audio_features']['audio_file'])
#print(type(propio_1['label']))
#print(type(propio_1['track_id']))
#print(propio_1)

# Features extracted manually
file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/COVERS80_3_extended/W_isOriginal_not_found/P_498783.h5'
propio_2 = dd.io.load(file_path)
#print(type(propio_2))
print(propio_2['audio_features']['audio_file'])
#print(type(propio_2['label']))
#print(type(propio_2['track_id']))
#print(propio_2)

# Features extracted manually
file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/COVERS80_3_extended/W_isOriginal_not_found/P_498787.h5'
propio_3 = dd.io.load(file_path)
#print(type(propio_2))
print(propio_3['audio_features']['audio_file'])
#print(type(propio_2['label']))
#print(type(propio_2['track_id']))
#print(propio_2)

# query cover song
query_audio = estd.MonoLoader(filename='/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Wish_You_Were_Here/pink_floyd+Wish_You_Were_Here+04-Wish_You_Were_Here.mp3', sampleRate=16000)()
print(type(query_audio))
print(query_audio.shape)

# Extracting HPCP features
query_hpcp = hpcpgram(query_audio, sampleRate=16000)
print(type(query_hpcp))

# Returns the audio, its sample rate and more.
query_audio_2 = estd.AudioLoader(filename='/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Wish_You_Were_Here/pink_floyd+Wish_You_Were_Here+04-Wish_You_Were_Here.mp3')()
query_audio_2_samples = len(query_audio_2[0])
duration_original = query_audio_2_samples / query_audio_2[1]
print(type(query_audio_2[0]))
print(query_audio_2[0].shape)

# Extracting HPCP features
query_hpcp_2 = hpcpgram(query_audio_2[0][:, 0], sampleRate=16000)
print((query_hpcp))

note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']


plt.figure()
plt.title(f"HPCP from query song 1", fontsize=20)
plt.imshow(query_hpcp[:1600].T, aspect='auto', origin='lower', interpolation='none', extent=[0, duration_original, -0.5, 11.5])
plt.xlabel('Time (seconds)', fontsize=20)
plt.xticks(fontsize=20)
plt.ylabel('HPCP Index (musical notes)', fontsize=20)
plt.yticks(range(12), note_names, fontsize=20)
plt.show(block=False)

plt.figure()
plt.title(f"HPCP from query song 2", fontsize=20)
plt.imshow(query_hpcp_2[:1600].T, aspect='auto', origin='lower', interpolation='none', extent=[0, duration_original, -0.5, 11.5])
plt.xlabel('Time (seconds)', fontsize=20)
plt.xticks(fontsize=20)
plt.ylabel('HPCP Index (musical notes)', fontsize=20)
plt.yticks(range(12), note_names, fontsize=20)
plt.show(block=False)


# Suponiendo que tienes una variable llamada hpcp_data que es un numpy.ndarray
# También tienes las etiquetas label y track_id

# Definir los datos
label = "W_6536"  # Ejemplo de etiqueta (ID del trabajo)
track_id = "P_6536"  # Ejemplo de ID de pista (ID de actuación)

# Crear un nuevo archivo HDF5
with h5py.File('/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIO/W_6536.h5', 'w') as f:
    # Guardar los datos de HPCP
    f.create_dataset('hpcp', data=song_hpcp)
    # Guardar la etiqueta y el ID de la pista
    f.attrs['label'] = label
    f.attrs['track_id'] = track_id

file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIO/W_6536.h5'
P_6536_data = dd.io.load(file_path)
print(type(P_6536_data))
print(P_6536_data)
print("caca")