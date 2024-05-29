import time
import math
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

import essentia.standard as estd
import essentia
from essentia.pytools.spectral import hpcpgram

# list_original_songs_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/list1.list'
# list_cover_songs_paths = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/list2.list'
# output_folder = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/COVERS80'

class Spectral_representations():
    
    def __init__(self):
        pass
    
    def extract_spectral_representations(self, song_path, resample_quality, min_frequency, max_frequency):
        
        # Load query audio with AudioLoader algorithm, it returns:
        # · [0] audio (vector_stereosample) - the input audio signal
        # · [1] sampleRate (real) - the sampling rate of the audio signal [Hz]
        # · [2] numberChannels (integer) - the number of channels
        # · [3] md5 (string) - the MD5 checksum of raw undecoded audio payload
        # · [4] bit_rate (integer) - the bit rate of the input audio, as reported by the decoder codec
        # · [5] codec (string) - the codec that is used to decode the input audio
        song_audio_features = estd.AudioLoader(filename = song_path)()
        
        sample_rate = song_audio_features[1]
        
        # Load song with MonoLoader algorithm, it returns:
        # · [0] audio (vector_real) - the audio signal
        song_audio = estd.MonoLoader(filename = song_path, resampleQuality = resample_quality, sampleRate = song_audio_features[1])()

        frame_size = sample_rate * 0.1
        frame_size = int(2 ** math.ceil(math.log2(frame_size)))
        hop_size = int(frame_size/2)
        
        # Extracting features from audio loaded with AudioLoader algorithm
        windowing = estd.Windowing(type='hamming', zeroPadding=frame_size)
        spectrum = estd.Spectrum()
        melbands = estd.MelBands(numberBands=96, lowFrequencyBound=min_frequency, highFrequencyBound=max_frequency)
        spectrum_logfreq = estd.LogSpectrum(binsPerSemitone=1)

        amp2db = estd.UnaryOperator(type='lin2db', scale=2)
        pool = essentia.Pool()

        for frame in estd.FrameGenerator(song_audio, frameSize=frame_size, hopSize=hop_size):
            frame_spectrum = spectrum(windowing(frame))
            frame_mel = melbands(frame_spectrum)
            frame_spectrum_logfreq, _, _ = spectrum_logfreq(frame_spectrum)

            pool.add('spectrum_db', amp2db(frame_spectrum))
            pool.add('mel96_db', amp2db(frame_mel))
            pool.add('spectrum_logfreq_db', amp2db(frame_spectrum_logfreq))
        
        y, sr = librosa.load(song_path)
        
        d = np.abs(librosa.stft(y)) # Obtener el espectrograma de magnitud
        db = librosa.amplitude_to_db(d, ref=np.max) # Convertir a escala de decibelios
        
        return pool, db, sr
