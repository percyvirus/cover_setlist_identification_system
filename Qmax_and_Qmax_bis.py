import numpy as np
import essentia.standard as estd

class Qmax_and_Qmax_bis:
    def __init__(self, binarize_percentile, frame_stack_size, frame_stack_stride, noti, oti, oti_binary, streaming, alignment_type, dis_extension, dis_onset, distance_type):
        self.binarize_percentile = binarize_percentile
        self.frame_stack_size = frame_stack_size
        self.frame_stack_stride = frame_stack_stride
        self.noti = noti
        self.oti = oti
        self.oti_binary = oti_binary
        self.streaming = streaming
        self.alignment_type = alignment_type
        self.dis_extension = dis_extension
        self.dis_onset = dis_onset
        self.distance_type = distance_type

    def execute_qmax_and_qmax_bis(self, hpcp1, hpcp2):
        # Placeholder code for demonstration purposes
        csm_crp = estd.ChromaCrossSimilarity(frameStackSize=self.frame_stack_size,
                                        frameStackStride=self.frame_stack_stride,
                                        binarizePercentile=self.binarize_percentile,
                                        noti=self.noti,
                                        oti=self.oti,
                                        otiBinary=self.oti_binary)

        pair_csm_crp = csm_crp(hpcp2, hpcp1)
        
        score_matrix, distance = estd.CoverSongSimilarity(disOnset=self.dis_onset,
                                                  disExtension=self.dis_extension,
                                                  alignmentType=self.alignment_type,
                                                  distanceType=self.distance_type)(pair_csm_crp)
        
        return pair_csm_crp, score_matrix, distance