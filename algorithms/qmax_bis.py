"""
Function for comparing cover songs based on Chroma features and similarity measures.
"""
import os
import time
import essentia.standard as estd
import numpy as np
import deepdish as dd


class Qmax_bis:
    def __init__(self):
        self.binarize_percentile = 0.095
        self.frame_stack_size = 9
        self.frame_stackStride = 1
        self.noti_12_bins  = 12
        self.noti_36_bins  = 36
        self.oti = True
        self.otiBinary = None
        self.streaming = False
        self.alignment_type = 'chen17'
        self.dis_extension = 0.5
        self.dis_onset = 0.5
        self.distance_type = 'asymmetric'

    def execute_qmax_bis(self, dataset, otiBinary, results_path):
        self.otiBinary = otiBinary  # Set Qmax or Qmax*
        confusion_matrix = {}
        confusion_matrix_12_bins = {}
        # confusion_matrix_36_bins = {}
        total_original_songs = 0
        total_cover_songs = 0
        
        for i, (label_id, original_song_track_id, original_song_data_dataset) in enumerate(dataset.iterate_original_songs_data()):
            # print(f"Work ID ({i}): {label_id} ({original_song_data_dataset['audio_features']['audio_file']})")
            print(f"Work ID ({i}): {label_id}")
            total_original_songs = total_original_songs + 1
            for j, (cover_song_track_id, cover_song_data_dataset) in enumerate(dataset.iterate_cover_songs_data()):
                if cover_song_track_id == "P_ID_not_found":
                    cover_song_track_id = "P_ID_not_found_"+cover_song_data_dataset['label']
                print(f"Performance ID ({j}): {cover_song_track_id}")
                if "hpcp" in original_song_data_dataset:    # dataset with only hpcp_12_bins or hpcp_36_bins
                    original_song_hpcp = original_song_data_dataset["hpcp"]
                    cover_song_hpcp = cover_song_data_dataset["hpcp"]
                    
                    # Compute Chroma Cross Similarity
                    cross_recurrence_plot, extraction_time_crp = self.compute_chroma_cross_similarity(original_song_hpcp, cover_song_hpcp,
                                                                                                      self.binarize_percentile, self.frame_stack_size,
                                                                                                      self.frame_stackStride, self.noti_12_bins,
                                                                                                      self.oti, self.otiBinary, self.streaming)
                    # Compute Cover Song Similarity Distance
                    _, distance, extraction_time_css = self.compute_cover_song_similarity_distance(self.dis_onset, self.dis_extension, self.alignment_type, self.distance_type, cross_recurrence_plot)
                    
                    key = (label_id, cover_song_track_id)
                    
                    confusion_matrix[key] = {
                        "original_song_data": original_song_data_dataset,
                        "cover_song_data": cover_song_data_dataset,
                        "cross_recurrence": cross_recurrence_plot.astype(np.bool_),
                        # "score_matrix": score_matrix,
                        "distance": distance,
                        "extraction_time_crp": extraction_time_crp,
                        "extraction_time_css": extraction_time_css,
                        "is_cover": original_song_data_dataset["label"]==cover_song_data_dataset["label"]   # Check if the actual cover is a true cover of original song
                    }
                    
                elif "hpcp_12_bins" in original_song_data_dataset and "hpcp_36_bins" in original_song_data_dataset:
                    original_song_hpcp_12_bins = original_song_data_dataset["hpcp_12_bins"]
                    # original_song_hpcp_36_bins = original_song_data_dataset["hpcp_36_bins"]
                    cover_song_hpcp_12_bins = cover_song_data_dataset["hpcp_12_bins"]
                    # cover_song_hpcp_36_bins = cover_song_data_dataset["hpcp_36_bins"]
                    
                    # Compute Chroma Cross Similarity
                    cross_recurrence_plot_12_bins, extraction_time_crp_12_bins = self.compute_chroma_cross_similarity(original_song_hpcp_12_bins, cover_song_hpcp_12_bins,
                                                                                                                      self.binarize_percentile, self.frame_stack_size,
                                                                                                                      self.frame_stackStride, self.noti_12_bins,
                                                                                                                      self.oti, self.otiBinary, self.streaming)
                    """cross_recurrence_plot_36_bins, extraction_time_crp_36_bins = self.compute_chroma_cross_similarity(original_song_hpcp_36_bins, cover_song_hpcp_36_bins,
                                                                                                                      self.binarize_percentile, self.frame_stack_size,
                                                                                                                      self.frame_stackStride, self.noti_36_bins,
                                                                                                                      self.oti, self.otiBinary, self.streaming)"""
                    
                    # Compute Cover Song Similarity Distance
                    _, distance_12_bins, extraction_time_css_12_bins = self.compute_cover_song_similarity_distance(self.dis_onset, self.dis_extension, self.alignment_type, self.distance_type, cross_recurrence_plot_12_bins)
                    # _, distance_36_bins, extraction_time_css_36_bins = self.compute_cover_song_similarity_distance(self.dis_onset, self.dis_extension, self.alignment_type, self.distance_type, cross_recurrence_plot_36_bins)
                    # Check if the actual cover is a true cover of original song
            
                    key = (label_id, cover_song_track_id)
                    
                    confusion_matrix_12_bins[key] = {
                        "original_song_audio_features": original_song_data_dataset["audio_features"],
                        "original_song_hpcp_features": original_song_data_dataset["hpcp_features"],
                        "original_song_second_hand_song_API_features": original_song_data_dataset["second_hand_song_API_features"],
                        "original_track_id": original_song_data_dataset["track_id"],
                        "cover_song_audio_features": cover_song_data_dataset["audio_features"],
                        "cover_song_hpcp_features": cover_song_data_dataset["hpcp_features"],
                        "cover_song_second_hand_song_API_features": cover_song_data_dataset["second_hand_song_API_features"],
                        "cover_track_id": cover_song_data_dataset["track_id"],
                        "cross_recurrence_plot": cross_recurrence_plot_12_bins.astype(np.bool_),
                        # "score_matrix": score_matrix_12_bins,
                        "distance": distance_12_bins,
                        "extraction_time_crp": extraction_time_crp_12_bins,
                        "extraction_time_css": extraction_time_css_12_bins,
                        "is_cover": original_song_data_dataset["label"]==cover_song_data_dataset["label"]   # Check if the actual cover is a true cover of original song
                    }
                    """confusion_matrix_36_bins[key] = {
                        "original_song_audio_features": original_song_data_dataset["audio_features"],
                        "original_song_hpcp_features": original_song_data_dataset["hpcp_features"],
                        "original_song_second_hand_song_API_features": original_song_data_dataset["second_hand_song_API_features"],
                        "original_track_id": original_song_data_dataset["track_id"],
                        "cover_song_audio_features": cover_song_data_dataset["audio_features"],
                        "cover_song_hpcp_features": cover_song_data_dataset["hpcp_features"],
                        "cover_song_second_hand_song_API_features": cover_song_data_dataset["second_hand_song_API_features"],
                        "cover_track_id": cover_song_data_dataset["track_id"],
                        "cross_recurrence_plot": cross_recurrence_plot_36_bins.astype(np.bool_),
                        # "score_matrix": score_matrix_36_bins,
                        "distance": distance_36_bins,
                        "extraction_time_crp": extraction_time_crp_36_bins,
                        "extraction_time_css": extraction_time_css_36_bins,
                        "is_cover": original_song_data_dataset["label"]==cover_song_data_dataset["label"]   # Check if the actual cover is a true cover of original song
                    }"""
                    
                else:
                    print("No HPCPs found")
            
            if i == 1:
                total_cover_songs = j+1
                    
        file_name = "Qmax_bis_12_bins.h5"
        file_path = os.path.join(results_path, file_name)
        if os.path.exists(file_path):
            base_name, extension = os.path.splitext(file_name)
            count = 1
            while os.path.exists(os.path.join(results_path, f"{base_name}_{count}{extension}")):
                count += 1
            new_file_name = f"{base_name}_{count}{extension}"
        else:
            new_file_name = file_name
                    
        if confusion_matrix:
            confusion_matrix["parameters"] = {
                        "binarize_percentile": self.binarize_percentile,
                        "frame_stack_size": self.frame_stack_size,
                        "frame_stackStride": self.frame_stackStride,
                        "noti": self.noti_12_bins,
                        "oti": self.oti,
                        "otiBinary": self.otiBinary,
                        "alignment_type": self.alignment_type,
                        "dis_extension": self.dis_extension,
                        "dis_onset": self.dis_onset,
                        "distance_type": self.distance_type
                    }
            confusion_matrix["dataset_info"] = {
                        "total_original_songs": total_original_songs,
                        "total_cover_songs": total_cover_songs,
                    }
            dd.io.save(os.path.join(results_path,new_file_name), confusion_matrix)
        if confusion_matrix_12_bins:
            confusion_matrix_12_bins["parameters"] = {
                        "binarize_percentile": self.binarize_percentile,
                        "frame_stack_size": self.frame_stack_size,
                        "frame_stackStride": self.frame_stackStride,
                        "noti": self.noti_12_bins,
                        "oti": self.oti,
                        "otiBinary": self.otiBinary,
                        "alignment_type": self.alignment_type,
                        "dis_extension": self.dis_extension,
                        "dis_onset": self.dis_onset,
                        "distance_type": self.distance_type
                    }
            confusion_matrix_12_bins["dataset_info"] = {
                        "total_original_songs": total_original_songs,
                        "total_cover_songs": total_cover_songs,
                    }
            print(os.path.join(results_path,new_file_name))
            dd.io.save(os.path.join(results_path,new_file_name), confusion_matrix_12_bins)
        """if confusion_matrix_36_bins:
            confusion_matrix_36_bins["parameters"] = {
                        "binarize_percentile": self.binarize_percentile,
                        "frame_stack_size": self.frame_stack_size,
                        "frame_stackStride": self.frame_stackStride,
                        "noti": self.noti_36_bins,
                        "oti": self.oti,
                        "otiBinary": self.otiBinary,
                        "alignment_type": self.alignment_type,
                        "dis_extension": self.dis_extension,
                        "dis_onset": self.dis_onset,
                        "distance_type": self.distance_type
                    }
            confusion_matrix_36_bins["dataset_info"] = {
                        "total_original_songs": total_original_songs,
                        "total_cover_songs": total_cover_songs,
                    }
            dd.io.save(os.path.join(results_path,new_file_name), confusion_matrix_36_bins)"""
        
    def compute_chroma_cross_similarity(self, original_song_hpcp, cover_song_hpcp, binarize_percentile, frame_stack_size, frame_stackStride, noti, oti, otiBinary, streaming):
        crp = estd.ChromaCrossSimilarity(binarizePercentile=binarize_percentile,
                                        frameStackSize=frame_stack_size,
                                        frameStackStride=frame_stackStride,
                                        noti=noti,
                                        oti=oti,
                                        otiBinary=otiBinary,
                                        streaming=streaming)
        
        start_time_crp = time.time()
        chroma_cross_similarity = crp(original_song_hpcp, cover_song_hpcp)
        end_time_crp = time.time()
        extraction_time_crp = end_time_crp - start_time_crp
        
        return chroma_cross_similarity, extraction_time_crp
    
    def compute_cover_song_similarity_distance(self, dis_onset, dis_extension, alignment_type, distance_type, cross_recurrence_plot):
        css = estd.CoverSongSimilarity(disOnset=dis_onset,
                                        disExtension=dis_extension,
                                        alignmentType=alignment_type,
                                        distanceType=distance_type)
        
        start_time_css = time.time()
        score_matrix, distance = css(cross_recurrence_plot)
        end_time_css = time.time()
        extraction_time_css = end_time_css - start_time_css
        
        return score_matrix, distance, extraction_time_css

