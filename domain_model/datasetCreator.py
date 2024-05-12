import os
import numpy as np
import time
from unidecode import unidecode
from domain_model.dataset import Dataset
from .HPCPExtractor import HPCPExtractor
from .CREMAExtractor import CREMAExtractor
from domain_model.second_hand_song_API import SecondHandSongsAPI

class DatasetCreator():
    def __init__(self, controller, feature_extractor_type):
        self.controller = controller
        if feature_extractor_type == "HPCP":
            self.feature_extractor = HPCPExtractor()
            self.dataset_12_bins = Dataset()
            self.dataset_36_bins = Dataset()
            self.dataset_extended = Dataset()
        elif feature_extractor_type == "CREMA":
            self.feature_extractor = CREMAExtractor()
            self.dataset = Dataset()
            self.dataset_extended = Dataset()
        else:
            raise ValueError("Unsupported feature extractor type")
        self.secondHandSongAPI = SecondHandSongsAPI()
        
    def create_dataset(self, list_original_performances):
        # Read the list of original performances
        with open(list_original_performances, 'r') as original_performances_file:
            original_performances = original_performances_file.read().splitlines()
            
        # Get base path of list_original_performances_path and list_cover_performances_path (in this case is the same)
        base_path = "/".join(list_original_performances.split("/")[:-1])
        
        failed_SHS_API_original_performances_list = []
        failed_SHS_API_cover_performances_list = []
        original_performances_that_are_not_original_performance_list = []
        cover_performances_that_are_not_cover_performance_list = []
        
        if isinstance(self.feature_extractor, HPCPExtractor):
            for original_performance in original_performances:
                print(f"\nOriginal performance: {original_performance}")
                # Get original_performance path
                original_performance_path = f"{base_path}/{original_performance}.mp3"
                
                original_performance_hpcp_12_bins, original_performance_hpcp_36_bins, original_performance_extraction_time_12_bins, original_performance_extraction_time_36_bins, original_performance_sample_rate, original_performance_frame_size, original_performance_hop_size, original_performance_min_frequency, original_performance_max_frequency, original_performance_number_channels, original_performance_md5, original_performance_bit_rate, original_performance_codec = self.feature_extractor.extract_HPCPs(original_performance_path, resample_quality=0)
                
                #original_performance_title, original_performance_performer, original_performance_performer_url, original_performance_url, original_performance_is_original, original_performance_track_ID, original_performance_work_ID, original_performance_work_url = self.get_performance_info(original_performance_path)
                original_performance_info = self.get_performance_info(original_performance_path)
                
                if original_performance_info == None:
                    print(f"Failed retrieving info from SHS API for original performance: {original_performance_path}")
                    print("Triying again...")
                    original_performance_info = self.get_performance_info(original_performance_path)
                    if original_performance_info == None:
                        failed_SHS_API_original_performances_list.append(original_performance_path)
                
                if original_performance_info != None:
                    original_performance_data_12_bins = {
                        "hpcp": np.array(original_performance_hpcp_12_bins),
                        "label": str("W_"+original_performance_info[6]),
                        "track_id": str("P_"+original_performance_info[5])
                    }
                    self.dataset_12_bins.add_data(original_performance_data_12_bins["track_id"], original_performance_data_12_bins)
                    
                    original_performance_data_36_bins = {
                        "hpcp": np.array(original_performance_hpcp_36_bins),
                        "label": str("W_"+original_performance_info[6]),
                        "track_id": str("P_"+original_performance_info[5])
                    }
                    self.dataset_36_bins.add_data(original_performance_data_36_bins["track_id"], original_performance_data_36_bins)
                    
                    original_performance_data_extended = {
                        "hpcp_12_bins": np.array(original_performance_hpcp_12_bins),
                        "hpcp_36_bins": np.array(original_performance_hpcp_36_bins),
                        "label": str("W_"+original_performance_info[6]),
                        "track_id": str("P_"+original_performance_info[5]),
                        "audio_features": {
                            "audio_file": str(original_performance.split('/')[-1]),
                            "sample_rate": np.float64(original_performance_sample_rate),
                            "number_channels": np.int32(original_performance_number_channels),
                            "md5": str(original_performance_md5),
                            "bit_rate": np.int32(original_performance_bit_rate),
                            "codec": str(original_performance_codec)
                        },
                        "hpcp_features": {
                            "frame_size": np.int32(original_performance_frame_size),
                            "hop_size": np.int32(original_performance_hop_size),
                            "min_frequency": np.float64(original_performance_min_frequency),
                            "max_frequency": np.float64(original_performance_max_frequency),
                            "extraction_time_12_bins": np.float64(original_performance_extraction_time_12_bins),
                            "extraction_time_36_bins": np.float64(original_performance_extraction_time_36_bins)
                        },
                        "second_hand_song_API_features": {
                            "title": str(original_performance_info[0]),
                            "performer": str(original_performance_info[1]),
                            "performer_URL": str(original_performance_info[2]),
                            "performance_URL": str(original_performance_info[3]),
                            "work_URL": str(original_performance_info[7]),
                            "is_original": np.bool_(original_performance_info[4])
                        }
                    }
                    self.dataset_extended.add_data(original_performance_data_extended["track_id"], original_performance_data_extended)
                    
                    if not original_performance_info[4]:
                        original_performances_that_are_not_original_performance_list.append(original_performance_path)
                        print(f"Supossed original performance that is not original (is cover): {original_performance_path}")
                    
                    original_performance_folder_path = f"{base_path}/{original_performance.split('/')[0]}/"
                    cover_performances = os.listdir(original_performance_folder_path)
                    cover_performances = [item for item in cover_performances if item.endswith('.mp3')] # To avoid '.DS_Store'
                    for cover_performance in cover_performances:
                        if cover_performance != f"{original_performance.split('/')[1]}.mp3":
                            print(f"Cover performance: {cover_performance}")
                            # Get cover_performance path
                            cover_performance_path = original_performance_folder_path+cover_performance
                            cover_performance_hpcp_12_bins, cover_performance_hpcp_36_bins, cover_performance_extraction_time_12_bins, cover_performance_extraction_time_36_bins, cover_performance_sample_rate, cover_performance_frame_size, cover_performance_hop_size, cover_performance_min_frequency, cover_performance_max_frequency, cover_performance_number_channels, cover_performance_md5, cover_performance_bit_rate, cover_performance_codec = self.feature_extractor.extract_HPCPs(cover_performance_path, resample_quality=0)
                    
                            # cover_performance_title, cover_performance_performer, cover_performance_performer_url, cover_performance_url, cover_performance_is_original, cover_performance_track_ID, cover_performance_work_ID, cover_performance_work_url = self.get_performance_info(cover_performance_path)
                            cover_performance_info = self.get_performance_info(cover_performance_path)
                            
                            if cover_performance_info == None:
                                print(f"Failed retrieving info from SHS API for cover performance: {cover_performance_path}")
                                print("Triying again...")
                                cover_performance_info = self.get_performance_info(cover_performance_path)
                                if cover_performance_info == None:
                                    failed_SHS_API_cover_performances_list.append(cover_performance_path)
                            
                            if cover_performance_info != None:
                                cover_performance_data_12_bins = {
                                    "hpcp": np.array(cover_performance_hpcp_12_bins),
                                    "label": str("W_"+cover_performance_info[6]),
                                    "track_id": str("P_"+cover_performance_info[5])
                                }
                                self.dataset_12_bins.add_data(cover_performance_data_12_bins["track_id"], cover_performance_data_12_bins)
                                
                                cover_performance_data_36_bins = {
                                    "hpcp": np.array(cover_performance_hpcp_36_bins),
                                    "label": str("W_"+cover_performance_info[6]),
                                    "track_id": str("P_"+cover_performance_info[5])
                                }
                                self.dataset_36_bins.add_data(cover_performance_data_36_bins["track_id"], cover_performance_data_36_bins)
                                
                                cover_performance_data_extended = {
                                    "hpcp_12_bins": np.array(cover_performance_hpcp_12_bins),
                                    "hpcp_36_bins": np.array(cover_performance_hpcp_36_bins),
                                    "label": str("W_"+cover_performance_info[6]),
                                    "track_id": str("P_"+cover_performance_info[5]),
                                    "audio_features": {
                                        "audio_file": str(cover_performance.split('.')[0]),
                                        "sample_rate": np.float64(cover_performance_sample_rate),
                                        "number_channels": np.int32(cover_performance_number_channels),
                                        "md5": str(cover_performance_md5),
                                        "bit_rate": np.int32(cover_performance_bit_rate),
                                        "codec": str(cover_performance_codec)
                                    },
                                    "hpcp_features": {
                                        "frame_size": np.int32(cover_performance_frame_size),
                                        "hop_size": np.int32(cover_performance_hop_size),
                                        "min_frequency": np.float64(cover_performance_min_frequency),
                                        "max_frequency": np.float64(cover_performance_max_frequency),
                                        "extraction_time_12_bins": np.float64(cover_performance_extraction_time_12_bins),
                                        "extraction_time_36_bins": np.float64(cover_performance_extraction_time_36_bins)
                                    },
                                    "second_hand_song_API_features": {
                                        "title": str(cover_performance_info[0]),
                                        "performer": str(cover_performance_info[1]),
                                        "performer_URL": str(cover_performance_info[2]),
                                        "performance_URL": str(cover_performance_info[3]),
                                        "work_URL": str(cover_performance_info[7]),
                                        "is_original": np.bool_(cover_performance_info[4])
                                    }
                                }
                                self.dataset_extended.add_data(cover_performance_data_extended["track_id"], cover_performance_data_extended)
                                
                                if cover_performance_info[4]:
                                    cover_performances_that_are_not_cover_performance_list.append(cover_performance_path)
                                    print(f"Supossed cover performance that is not cover (is original): {cover_performance_path}")
            
        elif isinstance(self.feature_extractor, CREMAExtractor):
            crema = self.feature_extractor.extract_CREMAs(original_performance, resample_quality=0)
            
            original_performance_ID = self.get_performance_info(original_performance_path)
            performance_data = {
                "crema": np.array(crema),
                "label": str("P_".join(original_performance_ID)),
                "track_id": str("W_".join(original_performance_ID))
            }
            self.dataset.add_data(performance_data["track_id"], performance_data)
                
            return self.dataset
                
        else:
            raise ValueError("Unsupported feature extractor type")
                 
        return self.dataset_12_bins, self.dataset_36_bins, self.dataset_extended, failed_SHS_API_original_performances_list, failed_SHS_API_cover_performances_list, original_performances_that_are_not_original_performance_list, cover_performances_that_are_not_cover_performance_list
        
            
    def get_performance_info(self, performance_path):
        # Extract information from the query song file name
        file_name_parts = performance_path.split('+')
        
        work_name = file_name_parts[0].split('/')[-2].replace('_', ' ').title()
        artist_name = file_name_parts[0].split('/')[-1].replace('_', ' ').title()
        performance_name = file_name_parts[2].split('-')[1].split('.')[0].replace('_s_', "'s_").replace('Don_t', "Don't").replace('Can_t', "Can't").replace('I_m', "I'm").replace('_', ' ').title()
        
        correct_performance = False
        correct_work = False
        
        results_performance = self.secondHandSongAPI.search_performance(performance_name, artist_name)
        time.sleep(3)
        results_work = self.secondHandSongAPI.search_work(work_name)
        time.sleep(3)
        if results_performance and results_work:
            # PERFORMANCE INFO
            if results_performance.get("totalResults", 0) == 0:
                results_performance_bis = self.secondHandSongAPI.search_performance(performance_name.replace('ing', "in'"), artist_name)
                time.sleep(8)
                if results_performance_bis.get("totalResults", 0) == 0:
                    performance_title = "performance_title_not_found"
                    performer = "performer_not_found"
                    performer_url = "performer_URL_not_found"
                    performance_url = "performance_URL_not_found"
                    is_original = False
                    performance_ID = "performance_ID_not_found"
                else:
                    result_performance_bis_page = results_performance_bis.get("resultPage", [])
                        
                    performance_title = result_performance_bis_page[0].get("title")
                    performer = result_performance_bis_page[0].get("performer", {}).get("name")
                    performer_url = result_performance_bis_page[0].get("performer", {}).get("uri")
                    performance_url = result_performance_bis_page[0].get("uri")
                    is_original = result_performance_bis_page[0].get("isOriginal")
                    performance_ID = self.secondHandSongAPI.extract_id(result_performance_bis_page[0].get("uri"))
            else:
                results_performance_page = results_performance.get("resultPage", [])
                
                for i, result_performance_page in enumerate(results_performance_page):
                    if not correct_performance:
                        if self.compare_strings(performance_name, result_performance_page.get("title")):
                            correct_performance = True
                            correct_performance_index = i
                        else:
                            correct_performance = False
                
                correct_performances_candidates = {}
                
                for k, result_performance_page_bis in enumerate(results_performance_page):
                    if self.compare_strings(performance_name, result_performance_page_bis.get("title")):
                        correct_performances_candidates.update({k: result_performance_page_bis})
                
                correct_performances_candidates_bis = {}
                
                for key, value in correct_performances_candidates.items():
                    if self.compare_strings(artist_name, value["performer"]["name"]):
                        correct_performances_candidates_bis.update({key: value["performer"]["name"]})

                fewest_words_count = float('inf')
                
                if len(correct_performances_candidates_bis) == 0:
                    for key, value in correct_performances_candidates.items():
                        words_count = len(value.get("title").split())
                        
                        if words_count < fewest_words_count:
                            fewest_words_count = words_count
                            key_fewest_words = key
                else:
                    for key, value in correct_performances_candidates_bis.items():
                        words_count = len(value.split())
                        
                        if words_count < fewest_words_count:
                            fewest_words_count = words_count
                            key_fewest_words = key
                
                if correct_performance:        
                    performance_title = results_performance_page[key_fewest_words].get("title")
                    performer = results_performance_page[key_fewest_words].get("performer", {}).get("name")
                    performer_url = results_performance_page[key_fewest_words].get("performer", {}).get("uri")
                    performance_url = results_performance_page[key_fewest_words].get("uri")
                    is_original = results_performance_page[key_fewest_words].get("isOriginal")
                    performance_ID = self.secondHandSongAPI.extract_id(results_performance_page[key_fewest_words].get("uri"))
                else:
                    performance_title = "performance_title_not_found"
                    performer = "performer_not_found"
                    performer_url = "performer_URL_not_found"
                    performance_url = "performance_URL_not_found"
                    is_original = False
                    performance_ID = "performance_ID_not_found"
            
            # WORK INFO
            if results_work.get("totalResults", 0) == 0:
                results_work_bis = self.secondHandSongAPI.search_work(work_name.replace('ing', "in'"))
                time.sleep(8)
                if results_work_bis.get("totalResults", 0) == 0:
                    work_ID = "work_ID_not_found"
                    work_url = "work_URL_not_found"
                else:
                    result_work_bis_page = results_work_bis.get("resultPage", [])
                    work_ID = self.secondHandSongAPI.extract_id(result_work_bis_page[0].get("uri"))
                    work_url = result_work_bis_page[0].get("uri")
            else:
                results_work_page = results_work.get("resultPage", [])
                
                for j, result_work_page in enumerate(results_work_page):
                    if not correct_work:
                        if self.compare_strings(work_name, result_work_page.get("title")):
                            correct_work = True
                            correct_work_index = j
                        else:
                            correct_work = False
                
                correct_works_candidates = {}
                
                for k, result_work_page_bis in enumerate(results_work_page):
                    if self.compare_strings(work_name, result_work_page_bis.get("title")):
                        correct_works_candidates.update({k: result_work_page_bis.get("title")})

                fewest_words_count = float('inf')
                for key, value in correct_works_candidates.items():
                    words_count = len(value.split())
                    
                    if words_count < fewest_words_count:
                        fewest_words_count = words_count
                        key_fewest_words = key
                
                if correct_work:   
                    # work_ID = self.secondHandSongAPI.extract_id(results_work_page[correct_work_index].get("uri"))
                    # work_url = results_work_page[correct_work_index].get("uri")
                    work_ID = self.secondHandSongAPI.extract_id(results_work_page[key_fewest_words].get("uri"))
                    work_url = results_work_page[key_fewest_words].get("uri")
                else:
                    work_ID = "work_ID_not_found"
                    work_url = "work_URL_not_found"
            
            return performance_title, performer, performer_url, performance_url, True, performance_ID, work_ID, work_url
            #return performance_title, performer, performer_url, performance_url, is_original, performance_ID, '158069', 'https://secondhandsongs.com/work/158069'
        else:
            print("No performances were found for the title '{}' performed by '{}'".format(performance_name, artist_name))
            return None
        
    def compare_strings(self, string1, string2):
        
        def clean_string(s):
            return unidecode(s.lower().replace('(', '').replace(')', '').replace(',', '').replace('!', ''))
        
        clean_string1 = clean_string(string1)
        clean_string2 = clean_string(string2)
    
        # Convert both strings to lowercase and split into words
        words1 = clean_string1.lower().split()
        words2 = clean_string2.lower().split()

        # Count the number of matching words
        matching_words_count = sum(1 for word in words1 if word in words2)

        # Return True if the number of matching words equals the number of words in string1
        return matching_words_count == len(words1)
        """
        # Identify the shorter and longer string
        string1 = string1.lower()
        string2 = string2.lower()
        
        if len(string1) > len(string2):
            short = string2
            long = string1
        else:
            short = string1
            long = string2

        # Compare substrings of the longer string with the shorter string
        for i in range(len(long) - len(short) + 1):
            if long[i:i+len(short)] == short:
                return True
        return False
        
            else:
                if results_work.get("totalResults", 0) == 0:
                        
                else:
                #total_results = results.get("totalResults", 0)
                #print("Total performances found:", total_results)
                results_performance_page = results_performance.get("resultPage", [])
                result_work_page = results_work.get("resultPage", [])
                for performance in results_performance_page:
                    performance_title = performance.get("title")
                    performer = performance.get("performer", {}).get("name")
                    performer_url = performance.get("performer", {}).get("uri")
                    performance_url = performance.get("uri")
                    is_original = performance.get("isOriginal")
                    performance_ID = self.secondHandSongAPI.extract_id(performance.get("uri"))
                    if results_work.get("totalResults", 0) == 0:
                        
                    else:
                        for work in result_work_page:
                            work_ID = self.secondHandSongAPI.extract_id(work.get("uri"))    # TODO: gestionar casos donde haya más de un resultado de work
                            work_url = work.get("uri")
                            return performance_title, performer, performer_url, performance_url, is_original, performance_ID, work_ID, work_url"""
        