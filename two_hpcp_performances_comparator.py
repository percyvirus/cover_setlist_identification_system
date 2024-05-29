import math
import essentia.standard as estd
from Qmax_and_Qmax_bis import Qmax_and_Qmax_bis
from hpcp import HPCP
from essentia.pytools.spectral import hpcpgram
import matplotlib.pyplot as plt
import deepdish as dd

performance_2_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended/W_4728/P_4728.h5'
performance_1_path = '/Users/percywbm/Desktop/PERCY/MÀSTER/DATASETS/PROPIOS/CUVERS80_extended/W_4728/P_5966.h5'

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

performance_1= dd.io.load(performance_1_path)
performance_2= dd.io.load(performance_2_path)

qmax_and_qmax_bis = Qmax_and_Qmax_bis(**params_qmax_and_qmax_bis)
csm_crp, score_matrix, distance = qmax_and_qmax_bis.execute_qmax_and_qmax_bis(performance_1['hpcp_12_bins'], performance_2['hpcp_12_bins'])

print("Distance:", distance)




