import essentia.standard as estd
from essentia.pytools.spectral import hpcpgram
import matplotlib.pyplot as plt
import numpy as np
from pylab import plot
import math
import os

folder_path = '/Users/percywbm/Desktop/PERCY/SONGS/Lodi'
output_folder = '/Users/percywbm/Desktop/PERCY/SONGS/Lodi/RESULTS_BIS'

time_plot = 0.05

# Set min and max frequency for HPCP calculation
min_frequency = 50
max_frequency = 5000

file_list = os.listdir(folder_path)
file_list = [filename for filename in file_list if filename.endswith('.mp3')]

num_wav_files = sum(1 for file in file_list if file.endswith('.mp3'))

distance_matrix = np.empty((4, num_wav_files + 1, num_wav_files + 1), dtype=object)
distance_matrix[0][0][0] = "Qmax_12_bins"
distance_matrix[1][0][0] = "Qmax_36_bins"
distance_matrix[2][0][0] = "Qmax_bis_12_bins"
distance_matrix[3][0][0] = "Qmax_bis_36_bins"

"""for i, audio_1_filename in enumerate(file_list):
    if audio_1_filename.endswith('.mp3'):
        for audio_2_filename in file_list[i:]:
            if audio_2_filename.endswith('.mp3'):
                print(audio_1_filename, audio_2_filename)"""

for i, audio_1_filename in enumerate([f for f in file_list if f.endswith('.mp3')]):
    for j, audio_2_filename in enumerate([g for g in file_list if g.endswith('.mp3')]):
        # if audio_1_filename != audio_2_filename:
        # for j, audio_2_filename in enumerate(file_list[i+1:]):
            # if audio_2_filename.endswith('.mp3'):
                
        audio_1_path = os.path.join(folder_path, audio_1_filename)
        audio_1_filename_without_extension = os.path.splitext(audio_1_filename)[0]
        
        audio_2_path = os.path.join(folder_path, audio_2_filename)
        audio_2_filename_without_extension = os.path.splitext(audio_2_filename)[0]
        
        for k in range(distance_matrix.shape[0]):
            distance_matrix[k, 0, i+1] = audio_1_filename_without_extension
            distance_matrix[k, j+1, 0] = audio_2_filename_without_extension
        
        print(f"referenceFeature: {audio_1_filename}")
        print(f"queryFeature: {audio_2_filename}")
        # Load audio 1
        audio_1_features = estd.AudioLoader(filename = audio_1_path)()
        # Load query audio with AudioLoader algorithm, it returns:
        # · [0] audio (vector_stereosample) - the input audio signal
        # · [1] sampleRate (real) - the sampling rate of the audio signal [Hz]
        # · [2] numberChannels (integer) - the number of channels
        # · [3] md5 (string) - the MD5 checksum of raw undecoded audio payload
        # · [4] bit_rate (integer) - the bit rate of the input audio, as reported by the decoder codec
        # · [5] codec (string) - the codec that is used to decode the input audio
        query_audio_1_samples = len(audio_1_features[0])
        duration_audio_1 = query_audio_1_samples / audio_1_features[1]
        audio_1 = estd.MonoLoader(filename=audio_1_path, sampleRate=audio_1_features[1])()

        """# Plot audio 1 in time domain
        time_axis_1 = np.linspace(0, duration_audio_1, query_audio_1_samples)
        plt.figure(figsize=(16, 9))
        plot(time_axis_1, audio_1)
        plt.title(f"'{audio_1_filename}' (audio 1)", fontsize=15)
        plt.grid()
        plt.xlim(0, duration_audio_1)
        plt.xlabel('Time (seconds)', fontsize=15)
        plt.ylabel('Amplitude', fontsize=15)
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}.png'))
        plt.show(block=False)"""

        # Load audio 2
        audio_2_features = estd.AudioLoader(filename = audio_2_path)()
        query_audio_2_samples = len(audio_2_features[0])
        duration_audio_2 = query_audio_2_samples / audio_2_features[1]
        audio_2 = estd.MonoLoader(filename=audio_2_path, sampleRate=audio_2_features[1])()

        """# Plot audio 2 in time domain
        time_axis_2 = np.linspace(0, duration_audio_2, query_audio_2_samples)
        plt.figure(figsize=(16, 9))
        plot(time_axis_2, audio_2)
        plt.title(f"'{audio_2_filename}' (audio 2)", fontsize=15)
        plt.grid()
        plt.xlim(0, duration_audio_1)
        plt.xlabel('Time (seconds)', fontsize=15)
        plt.ylabel('Amplitude', fontsize=15)
        plt.savefig(os.path.join(output_folder, f'{audio_2_filename_without_extension}.png'))
        plt.show(block=False)"""

        # HPCP query song 1
        frame_size_audio_1 = audio_1_features[1] * 0.1
        frame_size_audio_1 = int(2 ** math.ceil(math.log2(frame_size_audio_1)))
        hop_size_audio_1 = int(frame_size_audio_1/2)
        audio_1_hpcp_12_bins = hpcpgram(audio_1, sampleRate=audio_1_features[1], frameSize=frame_size_audio_1, hopSize=hop_size_audio_1, numBins=12, minFrequency=min_frequency, maxFrequency=max_frequency)
        audio_1_hpcp_36_bins = hpcpgram(audio_1, sampleRate=audio_1_features[1], frameSize=frame_size_audio_1, hopSize=hop_size_audio_1, numBins=36, minFrequency=min_frequency, maxFrequency=max_frequency)

        # HPCP query song 2
        frame_size_audio_2 = audio_2_features[1] * 0.1
        frame_size_audio_2 = int(2 ** math.ceil(math.log2(frame_size_audio_2)))
        hop_size_audio_2=int(frame_size_audio_2/2)
        audio_2_hpcp_12_bins = hpcpgram(audio_2, sampleRate=audio_2_features[1], frameSize=frame_size_audio_2, hopSize=hop_size_audio_2, numBins=12, minFrequency=min_frequency, maxFrequency=max_frequency)
        audio_2_hpcp_36_bins = hpcpgram(audio_2, sampleRate=audio_2_features[1], frameSize=frame_size_audio_2, hopSize=hop_size_audio_2, numBins=36, minFrequency=min_frequency, maxFrequency=max_frequency)

        note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        # Plotting the audio 1 HPCP features (12 bins)
        """plt.figure(figsize=(16, 9))
        plt.title(f"'{audio_1_filename}' (audio 1) HPCP 12 bins", fontsize=15)
        plt.imshow(audio_1_hpcp_12_bins.T, aspect='auto', origin='lower', interpolation='none', extent=[0, audio_1_hpcp_12_bins.shape[0], -0.5, 11.5])
        plt.xlabel('Frames', fontsize=15)
        plt.xticks(fontsize=15)
        plt.ylabel('HPCP Index (musical notes)', fontsize=15)
        plt.yticks(range(12), note_names, fontsize=15)
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_hpcp_12_bins.png'))
        plt.show(block=False)"""

        # Plotting the audio 1 HPCP features (36 bins)
        """plt.figure(figsize=(16, 9))
        plt.title(f"'{audio_1_filename}' (audio 1) HPCP 36 bins", fontsize=15)
        plt.imshow(np.roll(audio_1_hpcp_36_bins, 1, axis=1).T, aspect='auto', origin='lower', interpolation='none', extent=[0, audio_1_hpcp_12_bins.shape[0], -0.5, 11.5])
        plt.xlabel('Time (seconds)', fontsize=15)
        plt.xticks(fontsize=15)
        plt.ylabel('HPCP Index (musical notes)', fontsize=15)
        plt.yticks(range(12), note_names, fontsize=15)
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_hpcp_36_bins.png'))
        plt.show(block=False)"""

        # Plotting the audio 2 HPCP features (12 bins)
        """plt.figure(figsize=(16, 9))
        plt.title(f"'{audio_2_filename}' (audio 2) HPCP 12 bins", fontsize=15)
        plt.imshow(audio_2_hpcp_12_bins.T, aspect='auto', origin='lower', interpolation='none', extent=[0, hop_size_audio_1/audio_2_features[1]*audio_1_hpcp_12_bins.shape[0], -0.5, 11.5])
        plt.xlabel('Time (seconds)', fontsize=15)
        plt.xticks(fontsize=15)
        plt.ylabel('HPCP Index (musical notes)', fontsize=15)
        plt.yticks(range(12), note_names, fontsize=15)
        plt.savefig(os.path.join(output_folder, f'{audio_2_filename_without_extension}_hpcp_12_bins.png'))
        plt.show(block=False)"""

        """# Plotting the audio 2 HPCP features (36 bins)
        plt.figure(figsize=(16, 9))
        plt.title(f"'{audio_2_filename}' (audio 2) HPCP 36 bins", fontsize=15)
        plt.imshow(np.roll(audio_2_hpcp_36_bins, 1, axis=1).T, aspect='auto', origin='lower', interpolation='none', extent=[0, hop_size_audio_1/audio_2_features[1]*audio_1_hpcp_12_bins.shape[0], -0.5, 11.5])
        plt.xlabel('Time (seconds)', fontsize=15)
        plt.xticks(fontsize=15)
        plt.ylabel('HPCP Index (musical notes)', fontsize=15)
        plt.yticks(range(12), note_names, fontsize=15)
        plt.savefig(os.path.join(output_folder, f'{audio_2_filename_without_extension}_hpcp_36_bins.png'))
        plt.show(block=False)"""

        # Qmax
        # 12 bins
        # Compute binary chroma cross similarity
        csm_12_bins = estd.ChromaCrossSimilarity(frameStackSize=9,
                                        frameStackStride=1,
                                        binarizePercentile=0.095,
                                        noti=13,
                                        oti=True,
                                        otiBinary=True)

        oti_csm_12_bins = csm_12_bins(audio_2_hpcp_12_bins, audio_1_hpcp_12_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cross similarity matrix using OTI binary method (Qmax) 12 bins', fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 12 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 12 bins", fontsize=15)
        plt.imshow(oti_csm_12_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_csm_12_bins.png'))
        plt.show(block=False)"""
                    
        # Compute Cover Song Similarity Distance
        score_matrix_12_bins, distance_12_bins = estd.CoverSongSimilarity(disOnset=0.5,
                                                        disExtension=0.5,
                                                        alignmentType='serra09',
                                                        distanceType='asymmetric')(oti_csm_12_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cover song similarity distance with Qmax (12 bins): %s' % distance_12_bins, fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 12 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 12 bins", fontsize=15)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.imshow(score_matrix_12_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_Smith-Waterman_12_bins.png'))
"""
        # 36 bins
        # Compute binary chroma cross similarity
        csm_36_bins = estd.ChromaCrossSimilarity(frameStackSize=9,
                                        frameStackStride=1,
                                        binarizePercentile=0.095,
                                        noti=36,
                                        oti=True,
                                        otiBinary=True)

        oti_csm_36_bins = csm_36_bins(audio_2_hpcp_36_bins, audio_1_hpcp_36_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cross similarity matrix using OTI binary method (Qmax) 36 bins', fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 36 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 36 bins", fontsize=15)
        plt.imshow(oti_csm_36_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_csm_36_bins.png'))
        plt.show(block=False)
            """        
        # Compute Cover Song Similarity Distance
        score_matrix_36_bins, distance_36_bins = estd.CoverSongSimilarity(disOnset=0.5,
                                                        disExtension=0.5,
                                                        alignmentType='serra09',
                                                        distanceType='asymmetric')(oti_csm_36_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cover song similarity distance with Qmax (36 bins): %s' % distance_36_bins, fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 36 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 36 bins", fontsize=15)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.imshow(score_matrix_36_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_Smith-Waterman_36_bins.png'))
"""
        print(f"Qmax 12 bins distance: {distance_12_bins}")
        print(f"Qmax 36 bins distance: {distance_36_bins}")
        
        
        distance_matrix[0, j+1, i+1] = distance_12_bins
        distance_matrix[1, j+1, i+1] = distance_36_bins

        # Qmax*
        # 12 bins
        # Compute binary chroma cross similarity
        crp_12_bins = estd.ChromaCrossSimilarity(frameStackSize=9,
                                        frameStackStride=1,
                                        binarizePercentile=0.095,
                                        noti=12,
                                        oti=True)

        oti_crp_12_bins = crp_12_bins(audio_2_hpcp_12_bins, audio_1_hpcp_12_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cross similarity matrix using cross recurrent plot method (Qmax*) 12 bins', fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 12 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 12 bins", fontsize=15)
        plt.imshow(oti_crp_12_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_bis_csm_12_bins.png'))
        plt.show(block=False)
            """        
        # Compute Cover Song Similarity Distance
        score_matrix_12_bins, distance_12_bins = estd.CoverSongSimilarity(disOnset=0.5,
                                                        disExtension=0.5,
                                                        alignmentType='serra09',
                                                        distanceType='asymmetric')(oti_crp_12_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cover song similarity distance with Qmax* (12 bins): %s' % distance_12_bins, fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 12 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 12 bins", fontsize=15)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.imshow(score_matrix_12_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_bis_Smith-Waterman_12_bins.png'))
"""
        # 36 bins
        # Compute binary chroma cross similarity
        crp_36_bins = estd.ChromaCrossSimilarity(frameStackSize=9,
                                        frameStackStride=1,
                                        binarizePercentile=0.095,
                                        noti=36,
                                        oti=True)

        oti_crp_36_bins = crp_36_bins(audio_2_hpcp_36_bins, audio_1_hpcp_36_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cross similarity matrix using cross recurrent plot method (Qmax*) 36 bins', fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 36 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 36 bins", fontsize=15)
        plt.imshow(oti_crp_36_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_bis_csm_36_bins.png'))
        plt.show(block=False)
                   """ 
        # Compute Cover Song Similarity Distance
        score_matrix_36_bins, distance_36_bins = estd.CoverSongSimilarity(disOnset=0.5,
                                                        disExtension=0.5,
                                                        alignmentType='serra09',
                                                        distanceType='asymmetric')(oti_crp_36_bins)

        """plt.figure(figsize=(9, 9))
        plt.title('Cover song similarity distance with Qmax*(36 bins): %s' % distance_36_bins, fontsize=15)
        plt.xlabel(f"'{audio_2_filename}' (audio 2) HPCP 36 bins", fontsize=15)
        plt.ylabel(f"'{audio_1_filename}' (audio 1) HPCP 36 bins", fontsize=15)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.imshow(score_matrix_36_bins, origin='lower')
        plt.savefig(os.path.join(output_folder, f'{audio_1_filename_without_extension}_&_{audio_2_filename_without_extension}_Qmax_bis_Smith-Waterman_36_bins.png'))
"""
        print(f"Qmax* 12 bins distance: {distance_12_bins}")
        print(f"Qmax* 36 bins distance: {distance_36_bins}")
        
        distance_matrix[2, j+1, i+1] = distance_12_bins
        distance_matrix[3, j+1, i+1] = distance_36_bins
        
        #plt.close('all')
    
    
for layer in distance_matrix:
    mean_distance_list = []
    distance_array = np.array(layer)

    # distance_array[1:, 1:][distance_array[1:, 1:] == float('inf')] = 1
    # Obtener etiquetas y valores de la matriz
    labels = distance_array[0, 1:]
    values = distance_array[1:, 1:].astype(float)

    # Plotear la matriz de distancias
    plt.figure(figsize=(11, 8))
    plt.imshow(values, cmap='cool')

    # Añadir las etiquetas de los ejes
    plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45)
    plt.yticks(ticks=range(len(labels)), labels=labels)
    plt.xlabel('Signal 2 (referenceFeature)', fontsize=15)
    plt.ylabel('Signal 1 (queryFeature)', fontsize=15)
    plt.title(f'Distances Matrix {distance_array[0, 0]}', fontsize=15)

    # Añadir los valores en cada celda
    for i in range(len(labels)):
        for j in range(len(labels)):
            plt.text(j, i, format(values[i][j], '.6f'),
                    horizontalalignment='center',
                    color='white' if values[i][j] > 0.5 else 'black')
            if values[i][j] != float('inf'):
                mean_distance_list.append(values[i][j])

    mean_distance = sum(mean_distance_list) / len(mean_distance_list)
    """plt.text(-1, len(labels), f'Mean Distance: {mean_distance:.6f}',
         horizontalalignment='center', fontsize=12, color='red')"""
    
    plt.colorbar(label='Distance')
    plt.tight_layout()
    plt.show(block=False)
    plt.savefig(os.path.join(output_folder, f'distance_matrix_{distance_array[0, 0]}.png'))
    

plt.close('all')
               
"""for i in num_wav_files+1:
    for j in num_wav_files+1:
        distance_matrix[]
     """
#filename_without_extension = os.path.splitext(filename)[0]

#audio_path = os.path.join(folder_path, filename)

