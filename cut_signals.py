import librosa
import matplotlib.pyplot as plt
import numpy as np
import time
import math

import essentia.standard as estd
from essentia.pytools.spectral import hpcpgram

# Ruta al archivo de audio
audio_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/PITCH_SHIFTED/SAWTOOTH/sawtooth_233,1_Hz.wav'
output_audio_path = audio_path

song_audio_features = estd.AudioLoader(filename = audio_path)()
        
sample_rate = song_audio_features[1]
number_channels = song_audio_features[2]
md5 = song_audio_features[3]
bit_rate = song_audio_features[4]
codec = song_audio_features[5]

# Load song with MonoLoader algorithm, it returns:
# · [0] audio (vector_real) - the audio signal
song_audio = estd.MonoLoader(filename = audio_path, resampleQuality = 0, sampleRate = sample_rate)()

nonzero_indices = np.nonzero(song_audio)[0]

# Definir los índices de muestra de inicio y fin del recorte
# Samples
start = nonzero_indices[0]  # Índice de muestra de inicio
end = nonzero_indices[-1]   # Índice de muestra de fin

# Time
start = int(0*sample_rate)  # Índice de muestra de inicio
end = int(10*sample_rate)   # Índice de muestra de fin

# Recortar la señal de audio
trimmed_signal = song_audio[start:end]

# Crear un vector de tiempo para la visualización
time = np.linspace(0, len(trimmed_signal) / sample_rate, num=len(trimmed_signal))

# Visualizar la señal recortada
plt.figure(figsize=(10, 4))
plt.plot(time, trimmed_signal)
plt.xlabel('Tiempo (s)')
plt.ylabel('Amplitud')
plt.title('Señal de audio recortada')
plt.show(block=False)

print(f"Time: {time[-1]}")
print(f"Samples: {len(trimmed_signal)}")

writer = estd.MonoWriter(filename = output_audio_path, format = 'wav', sampleRate = 44100)
writer(trimmed_signal)
print("fin")
