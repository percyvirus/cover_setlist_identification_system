import os
import json
import deepdish as dd
import numpy as np
from itertools import islice

class StatisticalExtractor:
    def __init__(self):
        pass
    
    def calculate_metrics(self, confusion_matrix_path):
        try:
            confusion_matrix = dd.io.load(confusion_matrix_path)
            work_IDs, performances_IDs = self.get_IDs(confusion_matrix)
            
            mean_rank = self.calculate_mr(confusion_matrix, work_IDs, performances_IDs) # DONE
            mean_reciprocal_rank = self.calculate_mrr(confusion_matrix, work_IDs, performances_IDs) # DONE
            mean_average_precision = self.calculate_map(confusion_matrix, work_IDs, performances_IDs)   # DONE
            mean_recall = self.calculate_mean_recall(confusion_matrix, work_IDs, performances_IDs)   # DONE)
            top1 = self.calculate_top1(confusion_matrix, work_IDs, performances_IDs)    # DONE
            top10 = self.calculate_topk(confusion_matrix, work_IDs, performances_IDs, 10)   # DONE
            mean_extraction_time_crp_covers, mean_extraction_time_crp_no_covers, mean_extraction_time_css_covers, mean_extraction_time_css_no_covers = self.calculate_extraction_times(confusion_matrix, work_IDs, performances_IDs)    # DONE
            parameters = confusion_matrix['parameters']
            dataset_info = confusion_matrix['dataset_info']
            
            results = {
                "dataset_info": dataset_info,
                "MR": mean_rank,
                "MRR": mean_reciprocal_rank,
                "MAP": mean_average_precision,
                "Top_1": top1,
                "Top_10": top10,
                "Recall": mean_recall,
                "mean_extraction_time_crp_covers": mean_extraction_time_crp_covers,
                "mean_extraction_time_crp_no_covers": mean_extraction_time_crp_no_covers,
                "mean_extraction_time_css_covers": mean_extraction_time_css_covers,
                "mean_extraction_time_css_no_covers": mean_extraction_time_css_no_covers,
                "Qmax_parameters": parameters
            }
            
            file_path = f"{confusion_matrix_path.replace('.h5', '')}_results.json"
            
            with open(file_path, "w") as json_file:
                json.dump(results, json_file, indent=4)

            print("Results saved at", file_path)
            
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except IOError:
            print("Error opening the file.")
        except Exception as e:
            self.ui.display_error(f"Error loading dataset from h5 file: {str(e)}")
            return None
    
    """def get_IDs(self, confusion_matrix):
        work_IDs = []
        performances_IDs = []
        for key in confusion_matrix.keys():
            if isinstance(key, tuple) and len(key) == 2:
                work_ID, performances_ID = key
                if isinstance(work_ID, str) and isinstance(performances_ID, str):
                    work_IDs.append(work_ID)
                    performances_IDs.append(performances_ID)
        return work_IDs, performances_IDs"""
    
    def get_IDs(self, confusion_matrix):
        work_IDs = []
        performances_IDs = []
        for key in confusion_matrix.keys():
            if isinstance(key, tuple) and len(key) == 2:
                if key[0] not in work_IDs:
                    work_IDs.append(key[0])
                if key[1] not in performances_IDs:
                    performances_IDs.append(key[1])
                
        return work_IDs, performances_IDs
    
    def calculate_mr(self, confusion_matrix, work_IDs, performances_IDs):
        ranks = ()
        for work_ID in work_IDs:
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            for performances_ID in performances_IDs:
                print(performances_ID)
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)
        
            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            rank = [i + 1 for i, valor in enumerate(sorted_boolens_list) if valor]
            rank = sum(rank) / len(rank) if rank else 0
            ranks = ranks + (rank,)
        
        mean_rank = sum(ranks) / len(ranks)
        return mean_rank

    def calculate_mrr(self, confusion_matrix, work_IDs, performances_IDs):
        reciprocal_ranks = ()
        for work_ID in work_IDs:
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)
        
            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            rank = [i + 1 for i, valor in enumerate(sorted_boolens_list) if valor]
            reciprocal_rank = [1 / x for x in rank]
            reciprocal_rank = sum(reciprocal_rank) / len(reciprocal_rank) if reciprocal_rank else 0
            reciprocal_ranks = reciprocal_ranks + (reciprocal_rank,)
        
        mean_reciprocal_rank = sum(reciprocal_ranks) / len(reciprocal_ranks)
        return mean_reciprocal_rank

    def calculate_map(self, confusion_matrix, work_IDs, performances_IDs):
        average_precisions = ()
        for work_ID in work_IDs:
            Tp = 0
            Fp = 0
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)

            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            rank = [i + 1 for i, valor in enumerate(sorted_boolens_list) if valor]
            if rank[0] == 1:
                Tp = Tp + 1
            else:
                Fp = Fp + 1
            precison = Tp/(Tp+Fp)
            average_precisions = average_precisions + (precison,)

        mean_average_precision = sum(average_precisions) / len(average_precisions)
        return mean_average_precision


    def calculate_top1(self, confusion_matrix, work_IDs, performances_IDs):
        top1 = ()
        for work_ID in work_IDs:
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)

            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            rank = [i + 1 for i, valor in enumerate(sorted_boolens_list) if valor]
            if rank[0] == 1:
                top1 = top1 + (1,)
            else:
                top1 = top1 + (0,)

        top1 = sum(top1)
        return top1

    def calculate_topk(self, confusion_matrix, work_IDs, performances_IDs, k):
        top10 = ()
        for work_ID in work_IDs:
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            count = 0
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)

            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            rank = [i + 1 for i, valor in enumerate(sorted_boolens_list) if valor]
            for value in rank:
                if value <= k:
                    count += 1
            top10 = top10 + (count,)
            
        top10 = sum(top10)
        return top10
    
    def calculate_mean_recall(self, confusion_matrix, work_IDs, performances_IDs):
        recalls = ()
        for work_ID in work_IDs:
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)

            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            num_covers = sorted_boolens_list.count(True)
            top_num_covers = islice(sorted_boolens_list, num_covers)
            true_count = sum(1 for value in top_num_covers if value)
            recall = true_count/num_covers
            recalls = recalls + (recall,)

        mean_recall = sum(recalls) / len(recalls)
        return mean_recall
    
    def calculate_extraction_times(self, confusion_matrix, work_IDs, performances_IDs):
        extraction_times_crp_covers = ()
        extraction_times_crp_no_covers = ()
        extraction_times_css_covers = ()
        extraction_times_css_no_covers = ()
        for work_ID in work_IDs:
            tuples_list = ()
            distance_list = ()
            boolens_list = ()
            times_crp_list = ()
            times_css_list = ()
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)
                times_crp_list += (pair_of_songs['extraction_time_crp'],)
                times_css_list += (pair_of_songs['extraction_time_css'],)

            combined_list = list(zip(distance_list, tuples_list, boolens_list, times_crp_list, times_css_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list, sorted_times_crp_list, sorted_times_css_list = zip(*combined_list)
            total_true = sum(sorted_boolens_list)
            
            for _, _, is_cover, extraction_time_crp, extraction_time_css in zip(sorted_distance_list, sorted_tuples_list, sorted_boolens_list, sorted_times_crp_list, sorted_times_css_list):
                if is_cover:
                    extraction_times_crp_covers += (extraction_time_crp,)
                    extraction_times_css_covers += (extraction_time_css,)
                else:
                    extraction_times_crp_no_covers += (extraction_time_crp,)
                    extraction_times_css_no_covers += (extraction_time_css,)
                    
        mean_extraction_time_crp_covers = sum(extraction_times_crp_covers) / len(extraction_times_crp_covers) if extraction_times_crp_covers else 0
        mean_extraction_time_crp_no_covers = sum(extraction_times_crp_no_covers) / len(extraction_times_crp_no_covers) if extraction_times_crp_no_covers else 0
        
        mean_extraction_time_css_covers = sum(extraction_times_css_covers) / len(extraction_times_css_covers) if extraction_times_css_covers else 0
        mean_extraction_time_css_no_covers = sum(extraction_times_css_no_covers) / len(extraction_times_css_no_covers) if extraction_times_css_no_covers else 0
        
        return mean_extraction_time_crp_covers, mean_extraction_time_crp_no_covers, mean_extraction_time_css_covers, mean_extraction_time_css_no_covers
    
    
    def sort_results(self, confusion_matrix, work_IDs, performances_IDs):
        for work_ID in work_IDs:
            tuples_list = []
            distance_list = []
            boolens_list = []
            for performances_ID in performances_IDs:
                pair_of_songs = confusion_matrix[(work_ID, performances_ID)]
                tuples_list += ((work_ID, performances_ID),)
                distance_list += (pair_of_songs['distance'],)
                boolens_list += (pair_of_songs['is_cover'],)
                times_crp_list += (pair_of_songs['extraction_time_crp'],)
                times_css_list += (pair_of_songs['extraction_time_css'],)

            combined_list = list(zip(distance_list, tuples_list, boolens_list))
            combined_list.sort()
            sorted_distance_list, sorted_tuples_list, sorted_boolens_list = zip(*combined_list)
            return sorted_distance_list, sorted_tuples_list, sorted_boolens_list 