import time
import math

import essentia.standard as estd
from essentia.pytools.spectral import hpcpgram

# list_original_songs_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/list1.list'
# list_cover_songs_paths = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/list2.list'
# output_folder = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/COVERS80'

class HPCP():
    
    def __init__(self):
        pass
    
    def extract_HPCPs(self, song_path, resample_quality, num_bins, min_frequency, max_frequency):
        
        # Load query audio with AudioLoader algorithm, it returns:
        # · [0] audio (vector_stereosample) - the input audio signal
        # · [1] sampleRate (real) - the sampling rate of the audio signal [Hz]
        # · [2] numberChannels (integer) - the number of channels
        # · [3] md5 (string) - the MD5 checksum of raw undecoded audio payload
        # · [4] bit_rate (integer) - the bit rate of the input audio, as reported by the decoder codec
        # · [5] codec (string) - the codec that is used to decode the input audio
        song_audio_features = estd.AudioLoader(filename = song_path)()
        
        sample_rate = song_audio_features[1]
        number_channels = song_audio_features[2]
        md5 = song_audio_features[3]
        bit_rate = song_audio_features[4]
        codec = song_audio_features[5]
        
        # Load song with MonoLoader algorithm, it returns:
        # · [0] audio (vector_real) - the audio signal
        song_audio = estd.MonoLoader(filename = song_path, resampleQuality = resample_quality, sampleRate = song_audio_features[1])()

        frame_size = sample_rate * 0.1
        frame_size = int(2 ** math.ceil(math.log2(frame_size)))
        hop_size = int(frame_size/2)
        
        # Extracting HPCP features from audio loaded with AudioLoader algorithm
        start_time_12_bins = time.time()
        hpcp = hpcpgram(song_audio, sampleRate=sample_rate, frameSize=frame_size, hopSize=hop_size, numBins=num_bins, minFrequency=min_frequency, maxFrequency=max_frequency)
        end_time_12_bins = time.time()
        extraction_time_12_bins = end_time_12_bins - start_time_12_bins
        
        return hpcp
