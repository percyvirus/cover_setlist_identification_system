import math
import essentia.standard as estd
from Qmax_and_Qmax_bis import Qmax_and_Qmax_bis
from hpcp import HPCP
from essentia.pytools.spectral import hpcpgram
import matplotlib.pyplot as plt

performance_1_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Lodi/creedence_clearwater_revival+Live_in_Europe+08-Lodi.mp3'
performance_2_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/COVERS80/coversongs/covers32k/Lodi/tesla+Five_Man_Acoustic_Jam+09-Lodi.mp3'

resample_quality = 0
num_bins = 12
min_frequency = 20
max_frequency = 20000

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
hpcp1 = hpcp.extract_HPCPs(performance_1_path, resample_quality, num_bins, min_frequency, max_frequency)
hpcp2 = hpcp.extract_HPCPs(performance_2_path, resample_quality, num_bins, min_frequency, max_frequency)

qmax_and_qmax_bis = Qmax_and_Qmax_bis(**params_qmax_and_qmax_bis)
csm_crp, score_matrix, distance = qmax_and_qmax_bis.execute_qmax_and_qmax_bis(hpcp1, hpcp2)

print("Distance:", distance)



