import json
import deepdish as dd
import essentia.standard as estd
from essentia.pytools.spectral import hpcpgram
import h5py
import numpy as np
import matplotlib.pyplot as plt

# Set query audio path
query_audio_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Wish_You_Were_Here/pink_floyd+Wish_You_Were_Here+04-Wish_You_Were_Here.mp3'


# Load query audio with AudioLoader algorithm, it returns:
# · [0] audio (vector_stereosample) - the input audio signal
# · [1] sampleRate (real) - the sampling rate of the audio signal [Hz]
# · [2] numberChannels (integer) - the number of channels
# · [3] md5 (string) - the MD5 checksum of raw undecoded audio payload
# · [4] bit_rate (integer) - the bit rate of the input audio, as reported by the decoder codec
# · [5] codec (string) - the codec that is used to decode the input audio
query_audio_1 = estd.AudioLoader(filename=query_audio_path)()
query_audio_1_samples = len(query_audio_1[0])
duration_original = query_audio_1_samples / query_audio_1[1]

# Load query audio with MonoLoader algorithm, it returns:
# · audio (vector_real) - the audio signal
query_audio_2 = estd.MonoLoader(filename=query_audio_path, sampleRate=16000)()

# Extracting HPCP features from audio loaded with AudioLoader algorithm
print(type(query_audio_1[0][:, 0]))
print(len(query_audio_1[0][:, 0]))
query_hpcp_12_1 = hpcpgram(query_audio_1[0][:, 0], sampleRate=query_audio_1[1])
query_hpcp_36_1 = hpcpgram(query_audio_1[0][:, 0], sampleRate=query_audio_1[1], numBins=36)

# Extracting HPCP features from audio loaded with MonoLoader algorithm
# Here we need to know the sample rate beforehand
query_hpcp_2 = hpcpgram(query_audio_2, sampleRate=16000)

# Define the notes for the HPCP plot
note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

plt.figure()
plt.title(f"HPCP 12 bins from query audio 1", fontsize=20)
plt.imshow(query_hpcp_12_1[:len(query_hpcp_12_1)].T, aspect='auto', origin='lower', interpolation='none', extent=[0, len(query_audio_1[0]) / query_audio_1[1], -0.5, 11.5])
plt.xlabel('Time (seconds)', fontsize=20)
plt.xticks(fontsize=20)
plt.ylabel('HPCP Index (musical notes)', fontsize=20)
plt.yticks(range(12), note_names, fontsize=20)
plt.show(block=False)

plt.figure()
plt.title(f"HPCP 36 bins from query audio 1", fontsize=20)
plt.imshow(query_hpcp_36_1[:len(query_hpcp_36_1)].T, aspect='auto', origin='lower', interpolation='none', extent=[0, len(query_audio_1[0]) / query_audio_1[1], -0.5, 11.5])
plt.xlabel('Time (seconds)', fontsize=20)
plt.xticks(fontsize=20)
plt.ylabel('HPCP Index (musical notes)', fontsize=20)
plt.yticks(range(12), note_names, fontsize=20)
plt.show(block=False)

# Definir los datos
label = "W_6536"  # Ejemplo de etiqueta (ID del trabajo)
track_id = "P_6536" # Ejemplo de ID de pista (ID de actuación)

file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/W_6536_BIS.h5'

#----------------------------------------------
data_to_save = {
    'hpcp': np.array(query_hpcp_12_1),
    'label': str(label),
    'track_id': track_id
}
np.object = object 
dd.io.save(file_path, data_to_save)

propio_2 = dd.io.load(file_path)
print(type(propio_2['hpcp']))
print(type(propio_2['label']))
print(type(propio_2['track_id']))
print(type(propio_2))
print(propio_2)

#----------------------------------------------

file_path_2 = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/W_6536_BIS.h5'

data_to_save_2 = {
                    "hpcp_12_bins": np.array(query_hpcp_12_1),
                    "label": str("W_"+"211"),
                    "track_id": str("P_"+"211"),
                    "audio_features": {
                        "sample_rate": np.float64(16000),
                        "number_channels": np.int32(1),
                        "md5": str("md5"),
                        "bit_rate": np.int32(250),
                        "codec": str("codec")
                    },
                    "hpcp_features": {
                        "frame_size": np.int32(906),
                        "hop_size": np.int32(450),
                        "min_frequency": np.float64(50),
                        "max_frequency": np.float64(5000),
                        "extraction_time_12_bins": np.float64(0.125),
                        "extraction_time_36_bins": np.float64(0.135)
                    },
                    "second_hand_song_API_features": {
                        "title": str("tittle"),
                        "performer": str("performer"),
                        "url": str("url"),
                        "is_original": np.bool_(True)
                    }
                }
np.object = object 
dd.io.save(file_path_2, data_to_save_2)

propio_2 = dd.io.load(file_path_2)
print(type(propio_2['hpcp_12_bins']))
print(type(propio_2['label']))
print(type(propio_2['track_id']))
print(type(propio_2['hpcp_features']['frame_size']))
print(type(propio_2['hpcp_features']['min_frequency']))
print(type(propio_2['second_hand_song_API_features']['is_original']))
print(type(propio_2))
print(propio_2)



with h5py.File(file_path, 'w') as f:
    f.create_dataset('hpcp', data=query_hpcp_12_1)
    f.create_dataset('label', data=np.string_(label))
    f.create_dataset('track_id', data=np.string_(track_id))

# Features extracted manually
file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/W_6536_BIS.h5'
propio_2 = dd.io.load(file_path)
print(type(propio_2['hpcp']))
print(type(propio_2['label']))
print(type(propio_2['track_id']))
print(type(propio_2))
print(propio_2)

# Crear un nuevo archivo HDF5
with h5py.File('/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/W_6536_BIS.h5', 'w') as f:
    # Guardar los datos de HPCP
    f.create_dataset('hpcp', data=query_hpcp_12_1)
    # Guardar la etiqueta y el ID de la pista
    f.attrs['label'] = label
    f.attrs['track_id'] = track_id

file_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIO/W_6536_BIS.h5'
P_6536_data = dd.io.load(file_path)
print(type(P_6536_data))
print(P_6536_data)