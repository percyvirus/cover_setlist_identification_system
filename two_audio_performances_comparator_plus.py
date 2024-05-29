import math
import essentia.standard as estd
from Qmax_and_Qmax_bis import Qmax_and_Qmax_bis
from hpcp import HPCP
from spectral_representations import Spectral_representations
from essentia.pytools.spectral import hpcpgram
import essentia
import matplotlib.pyplot as plt
import os
import numpy as np
import librosa
import librosa.display

performance_2_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Happiness_is_a_Warm_Gun/beatles+White_Album_Disc_1+08-Happiness_is_a_Warm_Gun.mp3'
performance_1_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Happiness_is_a_Warm_Gun/tori_amos+Strange_Little_Girls+10-Happiness_is_a_Warm_Gun.mp3'

resample_quality = 0
num_bins = 12
min_frequency_1 = 50
max_frequency_1 = 5000
min_frequency_2 = 20
max_frequency_2 = 20000

params_qmax_and_qmax_bis = {
    'binarize_percentile': 0.095,
    'frame_stack_size': 9,
    'frame_stack_stride': 1,
    'noti': 12,
    'oti': True,
    'oti_binary': False,
    'streaming': False,
    'alignment_type': 'serra09',
    'dis_extension': 0.5,
    'dis_onset': 0.5,
    'distance_type': 'asymmetric'
}

hpcp = HPCP()
hpcp1_1 = hpcp.extract_HPCPs(performance_1_path, resample_quality, num_bins, min_frequency_1, max_frequency_1)
hpcp2_1 = hpcp.extract_HPCPs(performance_2_path, resample_quality, num_bins, min_frequency_1, max_frequency_1)
hpcp1_2 = hpcp.extract_HPCPs(performance_1_path, resample_quality, num_bins, min_frequency_2, max_frequency_2)
hpcp2_2 = hpcp.extract_HPCPs(performance_2_path, resample_quality, num_bins, min_frequency_2, max_frequency_2)

qmax_and_qmax_bis = Qmax_and_Qmax_bis(**params_qmax_and_qmax_bis)
csm_crp_1, score_matrix_1, distance_1 = qmax_and_qmax_bis.execute_qmax_and_qmax_bis(hpcp1_1, hpcp2_1)
csm_crp_2, score_matrix_2, distance_2 = qmax_and_qmax_bis.execute_qmax_and_qmax_bis(hpcp1_2, hpcp2_2)

note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

# Plotting the audio 1 HPCP features 1
plt.figure(figsize=(16, 9))
plt.title(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP 1", fontsize=15)
plt.imshow(hpcp1_1.T, aspect='auto', origin='lower', interpolation='none', extent=[0, hpcp1_1.shape[0], -0.5, 11.5])
plt.xlabel('Frames', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('HPCP Index (musical notes)', fontsize=15)
plt.yticks(range(12), note_names, fontsize=15)

# Plotting the audio 1 HPCP features 1
plt.figure(figsize=(16, 9))
plt.title(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP 1", fontsize=15)
plt.imshow(hpcp2_1.T, aspect='auto', origin='lower', interpolation='none', extent=[0, hpcp2_1.shape[0], -0.5, 11.5])
plt.xlabel('Frames', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('HPCP Index (musical notes)', fontsize=15)
plt.yticks(range(12), note_names, fontsize=15)

# Plotting the audio 1 HPCP features 2
plt.figure(figsize=(16, 9))
plt.title(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP 2", fontsize=15)
plt.imshow(hpcp1_2.T, aspect='auto', origin='lower', interpolation='none', extent=[0, hpcp1_2.shape[0], -0.5, 11.5])
plt.xlabel('Frames', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('HPCP Index (musical notes)', fontsize=15)
plt.yticks(range(12), note_names, fontsize=15)

# Plotting the audio 1 HPCP features 2
plt.figure(figsize=(16, 9))
plt.title(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP 2", fontsize=15)
plt.imshow(hpcp2_2.T, aspect='auto', origin='lower', interpolation='none', extent=[0, hpcp2_2.shape[0], -0.5, 11.5])
plt.xlabel('Frames', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('HPCP Index (musical notes)', fontsize=15)
plt.yticks(range(12), note_names, fontsize=15)

# Plotting the audio 1 HPCP features 2
plt.figure(figsize=(16, 9))
plt.title(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP 2 - HPCP 1", fontsize=15)
plt.imshow((hpcp1_2-hpcp1_1).T, aspect='auto', origin='lower', interpolation='none', extent=[0, (hpcp1_2-hpcp1_1).shape[0], -0.5, 11.5])
plt.xlabel('Frames', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('HPCP Index (musical notes)', fontsize=15)
plt.yticks(range(12), note_names, fontsize=15)

# Plotting the audio 1 HPCP features 2
plt.figure(figsize=(16, 9))
plt.title(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP 2 - HPCP 1", fontsize=15)
plt.imshow((hpcp2_2-hpcp2_1).T, aspect='auto', origin='lower', interpolation='none', extent=[0, (hpcp2_2-hpcp2_1).shape[0], -0.5, 11.5])
plt.xlabel('Frames', fontsize=15)
plt.xticks(fontsize=15)
plt.ylabel('HPCP Index (musical notes)', fontsize=15)
plt.yticks(range(12), note_names, fontsize=15)

plt.figure(figsize=(9, 9))
plt.title('Cross similarity matrix Qmax* 1', fontsize=15)
plt.xlabel(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP", fontsize=15)
plt.ylabel(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP", fontsize=15)
plt.imshow(csm_crp_1, origin='lower')

plt.figure(figsize=(9, 9))
plt.title('Cross similarity matrix Qmax* 2', fontsize=15)
plt.xlabel(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP", fontsize=15)
plt.ylabel(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP", fontsize=15)
plt.imshow(csm_crp_2, origin='lower')

plt.figure(figsize=(9, 9))
plt.title('Cross similarity matrix Qmax* difference', fontsize=15)
plt.xlabel(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP", fontsize=15)
plt.ylabel(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP", fontsize=15)
plt.imshow(csm_crp_2-csm_crp_1, origin='lower')

csm_crp_dif = csm_crp_2-csm_crp_1
dif = np.sum(csm_crp_dif)
print(f"Difference: {dif}")

suma_por_columna = np.sum(csm_crp_dif, axis=0)

# Calcular la suma acumulada a lo largo de las columnas
suma_acumulada = np.cumsum(suma_por_columna)

# Visualizar la evolución de la suma acumulada
plt.figure(figsize=(9, 9))
plt.plot(suma_acumulada)
plt.title('Difference CSM', fontsize=15)
plt.xlabel(f"'{os.path.basename(performance_1_path)}' (audio 1) CSM", fontsize=15)
plt.ylabel(f"'{os.path.basename(performance_2_path)}' (audio 2) CSM", fontsize=15)
plt.xlim(0, csm_crp_dif.shape[1])
plt.xticks(fontsize=15)
plt.yticks(fontsize=15)
plt.grid(True)

plt.figure(figsize=(9, 9))
plt.title('Cover song similarity distance with Qmax* 1: %s' % distance_1, fontsize=15)
plt.xlabel(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP", fontsize=15)
plt.ylabel(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP", fontsize=15)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.imshow(score_matrix_1, origin='lower')
max_indices_1 = np.argmax(score_matrix_1, axis=0)
plt.plot(max_indices_1, color='red', linewidth=1)

plt.figure(figsize=(9, 9))
plt.title('Cover song similarity distance with Qmax* 2: %s' % distance_2, fontsize=15)
plt.xlabel(f"'{os.path.basename(performance_1_path)}' (audio 1) HPCP", fontsize=15)
plt.ylabel(f"'{os.path.basename(performance_2_path)}' (audio 2) HPCP", fontsize=15)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.imshow(score_matrix_2, origin='lower')
max_indices_2 = np.argmax(score_matrix_2, axis=0)
plt.plot(max_indices_2, color='red', linewidth=1)



"""spectral_representations = Spectral_representations()

pool_1_1, db_1_1, sr_1_1 = spectral_representations.extract_spectral_representations(performance_1_path, resample_quality, min_frequency_1, max_frequency_1)
pool_2_1, db_2_1, sr_2_1 = spectral_representations.extract_spectral_representations(performance_2_path, resample_quality, min_frequency_1, max_frequency_1)
pool_1_2, db_1_2, sr_1_2 = spectral_representations.extract_spectral_representations(performance_1_path, resample_quality, min_frequency_2, max_frequency_2)
pool_2_2, db_2_2, sr_2_2 = spectral_representations.extract_spectral_representations(performance_2_path, resample_quality, min_frequency_2, max_frequency_2)


plt.figure(figsize=(14, 5))
librosa.display.specshow(db_1_1, sr=sr_1_1, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f"Spectrogram'{os.path.basename(performance_1_path)}' (audio 1) 1", fontsize=15)
plt.ylim([50, 5000])

plt.figure(figsize=(14, 5))
librosa.display.specshow(db_2_1, sr=sr_2_1, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f"Spectrogram'{os.path.basename(performance_2_path)}' (audio 2) 1", fontsize=15)
plt.ylim([20, 20000])

plt.figure(figsize=(14, 5))
librosa.display.specshow(db_1_2, sr=sr_1_2, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f"Spectrogram'{os.path.basename(performance_1_path)}' (audio 1) 2", fontsize=15)
plt.ylim([50, 5000])

plt.figure(figsize=(14, 5))
librosa.display.specshow(db_2_2, sr=sr_2_2, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f"Spectrogram'{os.path.basename(performance_2_path)}' (audio 2) 2", fontsize=15)
plt.ylim([20, 20000])

plt.figure(figsize=(14, 5))
librosa.display.specshow(db_1_2-db_1_1, sr=sr_1_1, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f"Spectrogram'{os.path.basename(performance_1_path)}' (audio 1) difference", fontsize=15)
plt.ylim([20, 20000])

plt.figure(figsize=(14, 5))
librosa.display.specshow(db_2_2-db_2_1, sr=sr_1_1, x_axis='time', y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title(f"Spectrogram'{os.path.basename(performance_2_path)}' (audio 2) difference", fontsize=15)
plt.ylim([20, 20000])

# Plot all spectrograms.
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 12))

fig.suptitle(f"'{os.path.basename(performance_1_path)}' (audio 1) 1", fontsize=15)

ax1.set_title("Log-spectrogram (amp2db)")
ax1.set_xlabel("Time (frames)")
ax1.set_ylabel("Frequency bins")
ax1.imshow(pool_1_1['spectrum_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax2.set_title("Mel log-spectrogram (amp2db)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Mel frequency bands")
ax2.imshow(pool_1_1['mel96_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax3.set_title("Log-frequency log-spectrogram (amp2db)")
ax3.set_xlabel("Time (frames)")
ax3.set_ylabel("Log-frequency bins")
ax3.imshow(pool_1_1['spectrum_logfreq_db'].T, aspect = 'auto', origin='lower', interpolation='none')

# Plot all spectrograms.
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 12))

fig.suptitle(f"'{os.path.basename(performance_1_path)}' (audio 2) 1", fontsize=15)

ax1.set_title("Log-spectrogram (amp2db)")
ax1.set_xlabel("Time (frames)")
ax1.set_ylabel("Frequency bins")
ax1.imshow(pool_2_1['spectrum_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax2.set_title("Mel log-spectrogram (amp2db)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Mel frequency bands")
ax2.imshow(pool_2_1['mel96_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax3.set_title("Log-frequency log-spectrogram (amp2db)")
ax3.set_xlabel("Time (frames)")
ax3.set_ylabel("Log-frequency bins")
ax3.imshow(pool_2_1['spectrum_logfreq_db'].T, aspect = 'auto', origin='lower', interpolation='none')

# Plot all spectrograms.
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 12))

fig.suptitle(f"'{os.path.basename(performance_1_path)}' (audio 1) 2", fontsize=15)

ax1.set_title("Log-spectrogram (amp2db)")
ax1.set_xlabel("Time (frames)")
ax1.set_ylabel("Frequency bins")
ax1.imshow(pool_1_2['spectrum_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax2.set_title("Mel log-spectrogram (amp2db)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Mel frequency bands")
ax2.imshow(pool_1_2['mel96_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax3.set_title("Log-frequency log-spectrogram (amp2db)")
ax3.set_xlabel("Time (frames)")
ax3.set_ylabel("Log-frequency bins")
ax3.imshow(pool_1_2['spectrum_logfreq_db'].T, aspect = 'auto', origin='lower', interpolation='none')

# Plot all spectrograms.
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 12))

fig.suptitle(f"'{os.path.basename(performance_1_path)}' (audio 2) 2", fontsize=15)

ax1.set_title("Log-spectrogram (amp2db)")
ax1.set_xlabel("Time (frames)")
ax1.set_ylabel("Frequency bins")
ax1.imshow(pool_2_2['spectrum_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax2.set_title("Mel log-spectrogram (amp2db)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Mel frequency bands")
ax2.imshow(pool_2_2['mel96_db'].T, aspect = 'auto', origin='lower', interpolation='none')

ax3.set_title("Log-frequency log-spectrogram (amp2db)")
ax3.set_xlabel("Time (frames)")
ax3.set_ylabel("Log-frequency bins")
ax3.imshow(pool_2_2['spectrum_logfreq_db'].T, aspect = 'auto', origin='lower', interpolation='none')

# Plot all spectrograms.
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 12))

fig.suptitle(f"'{os.path.basename(performance_1_path)}' (audio 1) difference", fontsize=15)

ax1.set_title("Log-spectrogram (amp2db)")
ax1.set_xlabel("Time (frames)")
ax1.set_ylabel("Frequency bins")
ax1.imshow((pool_1_2['spectrum_db']-pool_1_1['spectrum_db']).T, aspect = 'auto', origin='lower', interpolation='none')

ax2.set_title("Mel log-spectrogram (amp2db)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Mel frequency bands")
ax2.imshow((pool_1_2['mel96_db']-pool_1_1['mel96_db']).T, aspect = 'auto', origin='lower', interpolation='none')

ax3.set_title("Log-frequency log-spectrogram (amp2db)")
ax3.set_xlabel("Time (frames)")
ax3.set_ylabel("Log-frequency bins")
ax3.imshow((pool_1_2['spectrum_logfreq_db']-pool_1_1['spectrum_logfreq_db']).T, aspect = 'auto', origin='lower', interpolation='none')

# Plot all spectrograms.
fig, ((ax1, ax2, ax3)) = plt.subplots(3, 1, sharex=True, sharey=False, figsize=(15, 12))

fig.suptitle(f"'{os.path.basename(performance_1_path)}' (audio 2) difference", fontsize=15)

ax1.set_title("Log-spectrogram (amp2db)")
ax1.set_xlabel("Time (frames)")
ax1.set_ylabel("Frequency bins")
ax1.imshow((pool_2_2['spectrum_db']-pool_2_1['spectrum_db']).T, aspect = 'auto', origin='lower', interpolation='none')

ax2.set_title("Mel log-spectrogram (amp2db)")
ax2.set_xlabel("Time (frames)")
ax2.set_ylabel("Mel frequency bands")
ax2.imshow((pool_2_2['mel96_db']-pool_2_1['mel96_db']).T, aspect = 'auto', origin='lower', interpolation='none')

ax3.set_title("Log-frequency log-spectrogram (amp2db)")
ax3.set_xlabel("Time (frames)")
ax3.set_ylabel("Log-frequency bins")
ax3.imshow((pool_2_2['spectrum_logfreq_db']-pool_2_1['spectrum_logfreq_db']).T, aspect = 'auto', origin='lower', interpolation='none')"""

plt.show()

print("Distance 1:", distance_1)
print("Distance 2:", distance_2)




