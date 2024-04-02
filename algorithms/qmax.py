"""
Function for comparing cover songs based on Chroma features and similarity measures.
With plots.
"""
import os
import time
import essentia.standard as estd
from essentia.standard import MonoLoader, ChromaCrossSimilarity, CoverSongSimilarity, Windowing, Spectrum
from essentia.pytools.spectral import hpcpgram
# pylab contains the plot() function, as well as figure, etc... (same names as Matlab)
from pylab import plot, show, figure, imshow
from essentia.standard import *
from tabulate import tabulate
# %matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# Define a function to print elapsed time
def print_elapsed_time(start_time, label):
    elapsed_time = time.time() - start_time
    print(f"{label}: {elapsed_time:.4f} seconds")

# Calculates the recall and return the number of covers present in dataset per actual original song.
def calculate_recall(sorted_distances, original_song_name_to_count):
    tp = 0
    fp = 0
    fn = 0
    
    # Count the number of relevant covers
    count = sum(1 for entry in sorted_distances if entry['cover_song_name'] == original_song_name_to_count)
    print(f"The original song '{original_song_name_to_count}' appears {count} times in sorted_distances.")

    top_cover_songs = [entry['cover_song_name'] for entry in sorted_distances[:count]]
    
    for cover_song in top_cover_songs:
        if cover_song in original_song_name_to_count:
            tp += 1
        else:
            fp += 1

    fn = max(0, count - tp)
    
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0

    return count, recall

def Qmax(list_original_songs_path, list_cover_songs_paths, output_folder):
    # Read the list of original songs
    with open(list_original_songs_path, 'r') as original_songs_file:
        original_songs = original_songs_file.read().splitlines()
    
    all_recall_values = []
    
    for original_song_path in original_songs:
        print(f"Original: {original_song_path}\n")
        # Load the query original song audio file
        # Use the full path from the list directly
        # Construct the full path of the list file
        # Obtener la ruta base des list1.list
        base_path = "/".join(list_original_songs_path.split("/")[:-1])
        
        # Combinar la ruta base con el segundo string (canción) y agregar la extensión ".mp3"
        original_song_path = f"{base_path}/{original_song_path}.mp3"
        print(original_song_path)
        
        # Construct the full path of the list file
        cover_songs_path = os.path.dirname(list_cover_songs_paths)
        
        # Extract information from the query original song file name
        original_song_data = []
        original_file_name_parts = original_song_path.split('+')
        original_artist_name = original_file_name_parts[0].split('/')[-1]
        original_album_name = original_file_name_parts[1]
        original_track_number = original_file_name_parts[2].split('-')[0]
        original_song_name = original_file_name_parts[2].split('-')[1].split('.')[0]

        original_song_data.append({
            'song_name': original_song_name,
            'artist_name': original_artist_name,
            'album_name': original_album_name,
            'track_number': original_track_number,
            'track_path': original_song_path
        })

        distances = []
        
        # Returns the audio, its sample rate and more.
        original_song_monoAudioFeat = essentia.standard.AudioLoader(filename=os.path.abspath(original_song_path))()
        original_song_samples = len(original_song_monoAudioFeat[0])
        duration_original = original_song_samples / original_song_monoAudioFeat[1]

        start_time_a = time.time()
        query_audio = estd.MonoLoader(filename=os.path.abspath(original_song_path), sampleRate=original_song_monoAudioFeat[1])()
        print_elapsed_time(start_time_a, "Loading query audio: ")
        
        # Converts x-axis from samples to time
        time_axis = np.linspace(0, duration_original, original_song_samples)
        
        plt.figure()
        plot(time_axis, query_audio)
        plt.title(f"Original song {original_song_name} by {original_artist_name}")
        plt.grid()
        plt.xlim(0, duration_original)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.show(block=False)

        # Read the list of covers file
        with open(list_cover_songs_paths, 'r') as cover_songs_file:
            lines = cover_songs_file.readlines()
            
        # Compute Harmonic Pitch Class Profile (HPCP) chroma features from original song.
        query_hpcp_start_time = time.time()
        query_hpcp = hpcpgram(query_audio, sampleRate=original_song_monoAudioFeat[1])
        print_elapsed_time(query_hpcp_start_time, "Calculating query_hpcp")
        
        original_song_samples = len(query_hpcp)
        note_names = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

        plt.figure()
        plt.title(f"HPCP from original song {original_song_name} by {original_artist_name}", fontsize=20)
        plt.imshow(query_hpcp[:original_song_samples].T, aspect='auto', origin='lower', interpolation='none', extent=[0, duration_original, -0.5, 11.5])
        plt.xlabel('Time (seconds)', fontsize=20)
        plt.xticks(fontsize=20)
        plt.ylabel('HPCP Index (musical notes)', fontsize=20)
        plt.yticks(range(12), note_names, fontsize=20)
        plt.show(block=False)
        
        plt.figure()
        plt.title(f"HPCP from original song {original_song_name} by {original_artist_name} (0.1 seconds)", fontsize=20)
        plt.imshow(query_hpcp[:original_song_samples].T, aspect='auto', origin='lower', interpolation='none', extent=[0, duration_original, -0.5, 11.5])
        plt.xlabel('Time (seconds)', fontsize=20)
        plt.xticks(fontsize=20)
        plt.ylabel('HPCP Index (musical notes)', fontsize=20)
        plt.yticks(range(12), note_names, fontsize=20)
        plt.xlim(33.96, 38.06)
        plt.show(block=False)
        
        w = Windowing(type = 'hann')
        spectrum = Spectrum()
        
        frame = query_audio[int(33.96*original_song_monoAudioFeat[1]):int(38.06*original_song_monoAudioFeat[1])]
        spec = spectrum(w(frame))
        
        plt.figure()
        plot(spec)
        plt.title("The spectrum original song (0.1 seconds):", fontsize=20)
        plt.ylim(0, np.max(spec[0:1000]))
        plt.grid()
        # Set x-axis to logarithmic scale
        plt.xscale('log')
        plt.xlim(10, 1000)
        plt.xlabel('Frequency (Hz)', fontsize=20)
        plt.ylabel('Magnitude', fontsize=20)
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.show(block=False)
        
        for line in lines:
            print(f"\nCover: {line}", end=' ')
            line = line.strip()
            parts = line.split('/')

            # Extract information from the file name (original song)
            cover_song_data = []
            cover_file_name_parts = parts[1].split('+')
            cover_artist_name = cover_file_name_parts[0]
            cover_album_name = cover_file_name_parts[1]
            cover_track_number = cover_file_name_parts[2].split('-')[0]
            cover_song_name = cover_file_name_parts[2].split('-')[1]

            cover_song_data.append({
                'song_name': cover_song_name,
                'artist_name': cover_artist_name,
                'album_name': cover_album_name,
                'track_number': cover_track_number,
                'track_path': os.path.join(cover_songs_path+'/'+line+'.mp3')
            })
            
            cover_song_monoAudioFeat = essentia.standard.AudioLoader(filename=cover_song_data[0]['track_path'])()
            
            print(f"Sample rate cover song: {cover_song_monoAudioFeat[1]} Hz.")
            cover_song_samples = len(cover_song_monoAudioFeat[0])
            print(f"# samples cover song: {cover_song_samples} samples.")
            duration_cover = cover_song_samples / cover_song_monoAudioFeat[1]
            print(f"Duration cover song: {duration_cover} seconds.")

            start_time_a = time.time()
            query_audio = estd.MonoLoader(filename=os.path.abspath(original_song_path), sampleRate=cover_song_monoAudioFeat[1])()
            print_elapsed_time(start_time_a, "Loading query audio")
            
            time_axis = np.linspace(0, duration_cover, len(query_audio))

            # Load the cover song audio file
            cover_song_audio = estd.MonoLoader(filename=cover_song_data[0]['track_path'], sampleRate=cover_song_monoAudioFeat[1])()

            plt.figure()
            plot(time_axis, query_audio)
            plt.title(f"Cover song {cover_song_name} by {cover_artist_name}")
            plt.grid()
            plt.xlabel('Time (seconds)')
            plt.ylabel('Amplitude')
            plt.xlim(0, duration_cover)
            plt.show(block=False)
            
            # Compute cover song HPCP Chroma features
            cover_song_hpcp_start_time = time.time()
            cover_song_hpcp = hpcpgram(cover_song_audio, sampleRate=cover_song_monoAudioFeat[1])
            print_elapsed_time(cover_song_hpcp_start_time, "Calculating cover_song_hpcp")
            
            cover_song_hpcp_samples = len(cover_song_hpcp)
            
            plt.figure()
            plt.title(f"HPCP from cover song {cover_song_name} by {cover_artist_name}", fontsize=20)
            plt.imshow(cover_song_hpcp[:cover_song_hpcp_samples].T, aspect='auto', origin='lower', interpolation='none', extent=[0, duration_cover, -0.5, 11.5])
            plt.xlabel('Time (seconds)', fontsize=20)
            plt.xticks(fontsize=20)
            plt.ylabel('HPCP Index (musical notes)', fontsize=20)
            plt.yticks(range(12), note_names, fontsize=20)
            plt.show(block=False)
            
            plt.figure()
            plt.title(f"HPCP from cover song {cover_song_name} by {cover_artist_name} (0.1 seconds)", fontsize=20)
            plt.imshow(cover_song_hpcp[:cover_song_hpcp_samples].T, aspect='auto', origin='lower', interpolation='none', extent=[0, duration_cover, -0.5, 11.5])
            plt.xlabel('Time (seconds)', fontsize=20)
            plt.xticks(fontsize=20)
            plt.ylabel('HPCP Index (musical notes)', fontsize=20)
            plt.yticks(range(12), note_names, fontsize=20)
            plt.xlim(32, 36.1)
            plt.show(block=False)
            
            w = Windowing(type = 'hann')
            spectrum = Spectrum()
            
            frame = cover_song_audio[int(32*cover_song_monoAudioFeat[1]):int(36.1*cover_song_monoAudioFeat[1])]
            spec = spectrum(w(frame))
            
            plt.figure()
            plot(spec)
            plt.title("The spectrum of cover (0.1 seconds):", fontsize=20)
            plt.ylim(0, np.max(spec[0:1000]))
            plt.grid()
            # Set x-axis to logarithmic scale
            plt.xscale('log')
            plt.xlim(10, 1000)
            plt.xlabel('Frequency (Hz)', fontsize=20)
            plt.ylabel('Magnitude', fontsize=20)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.show(block=False)
            
            # Compute Chroma Cross Similarity
            crp_start_time = time.time()
            crp = estd.ChromaCrossSimilarity(frameStackSize=9,
                                            frameStackStride=1,
                                            binarizePercentile=0.095,
                                            oti=True)

            cross_recurrence_plot = crp(query_hpcp, cover_song_hpcp)
            print_elapsed_time(crp_start_time, "Calculating Chroma Cross Similarity")
            
            plt.figure()
            plt.title('Cross recurrent plot [1]')
            plt.xlabel(f"Cover song {cover_song_name} by {cover_artist_name}")
            plt.ylabel(f"original song {original_song_name} by {original_artist_name}")
            plt.imshow(cross_recurrence_plot, origin='lower', extent=[0, duration_cover, 0, duration_original])
            plt.show(block=False)
            
            # Compute Cover Song Similarity Distance
            cover_song_similarity_start_time = time.time()
            score_matrix, distance = estd.CoverSongSimilarity(disOnset=0.5,
                                                            disExtension=0.5,
                                                            alignmentType='serra09',
                                                            distanceType='asymmetric')(cross_recurrence_plot)
            print_elapsed_time(cover_song_similarity_start_time, "Calculating Cover Song Similarity Distance")
            
            plt.figure()
            plt.title('Cover song similarity distance: %s' % distance, fontsize=20)
            plt.xlabel(f"Cover song {cover_song_name} by {cover_artist_name}", fontsize=20)
            plt.ylabel(f"original song {original_song_name} by {original_artist_name}", fontsize=20)
            plt.xticks(fontsize=20)
            plt.yticks(fontsize=20)
            plt.imshow(score_matrix, origin='lower', extent=[0, duration_cover, 0, duration_original])

            print('Cover song similarity distance: %s' % distance)

            # Append the results to the distances list
            distances.append({
            'cover_song_name': cover_song_name,
            'cover_artist_name': cover_artist_name,
            'distance': distance
            })

        # Sort the list of distances based on the 'distance' key
        sorted_distances = sorted(distances, key=lambda x: x['distance'])
        
        print(f"Original song {original_song_data[0]['song_name']} by {original_song_data[0]['artist_name']} distances to:")
    
        # Display the sorted distances in a table
        table_headers = ['Cover Song', 'Artist', 'Distance']
        table_data = [(entry['cover_song_name'], entry['cover_artist_name'], entry['distance']) for entry in sorted_distances]

        table = tabulate(table_data, headers=table_headers, tablefmt='grid')
        print(table)

        # Extract relevant cover songs for the current original song
        original_song_name_to_count = original_song_data[0]['song_name']

        # Calculate precision and recall
        count, recall_values = calculate_recall(sorted_distances, original_song_name_to_count)

        # Append precision and recall values to the lists
        all_recall_values.append(recall_values)

        # Print the recall for the current original song
        # print(f"Original song {original_song_data[0]['song_name']} by {original_song_data[0]['artist_name']}:")
        print(f"Recall: {recall_values}\n")
        
        # Construct the output file path
        output_file_path = os.path.join(output_folder, f'{original_artist_name}_{original_song_name}_distances.txt')

        # Save the results to a text file
        with open(output_file_path, 'w') as output_file:
            output_file.write(f"{original_song_name_to_count} by {original_song_data[0]['artist_name']}:\nHas a total of {count} covers.\n")
            output_file.write(f"Recall: {recall_values}.\n")
            output_file.write(f"These are the distances to all covers in dataset:\n")
            table_headers = ['Cover Song', 'Artist', 'Distance']
            table_data = [(entry['cover_song_name'], entry['cover_artist_name'], entry['distance']) for entry in sorted_distances]
            table = tabulate(table_data, headers=table_headers, tablefmt='grid')
            output_file.write(table)
    
    # Calculate Mean Recall across all original songs
    mean_recall_all = sum(all_recall_values) / len(all_recall_values) if len(all_recall_values) > 0 else 0

    # Print the overall Mean Recall
    print(f"Overall Mean Recall: {mean_recall_all:.4f}")

    # Write Mean Recall to a file
    output_summary_file_path = os.path.join(output_folder, 'summary.txt')
    with open(output_summary_file_path, 'w') as summary_file:
        summary_file.write(f"Overall Mean Recall: {mean_recall_all:.4f}\n")

    print(f"Results summary written to {output_summary_file_path}")
