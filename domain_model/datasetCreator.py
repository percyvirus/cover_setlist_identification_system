import os
import numpy as np
import time
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
        
    def create_dataset(self, list_original_songs):
        # Read the list of original songs
        with open(list_original_songs, 'r') as original_songs_file:
            original_songs = original_songs_file.read().splitlines()
            
        # Get base path of list_original_songs_path and list_cover_songs_path (in this case is the same)
        base_path = "/".join(list_original_songs.split("/")[:-1])
        
        if isinstance(self.feature_extractor, HPCPExtractor):
            for original_song in original_songs:
                print(f"\nOriginal song: {original_song}")
                # Get original_song path
                original_song_path = f"{base_path}/{original_song}.mp3"
                
                hpcp_12_bins, hpcp_36_bins, extraction_time_12_bins, extraction_time_36_bins, sample_rate, frame_size, hop_size, min_frequency, max_frequency, number_channels, md5, bit_rate, codec = self.feature_extractor.extract_HPCPs(original_song_path, resample_quality=0)
                
                original_song_title, original_song_performer, original_song_url, original_song_is_original, original_song_ID = self.get_song_info(original_song_path)
                
                song_data_12_bins = {
                    "hpcp": np.array(hpcp_12_bins),
                    "label": str("W_"+original_song_ID),
                    "track_id": str("P_"+original_song_ID)
                }
                self.dataset_12_bins.add_data(song_data_12_bins["track_id"], song_data_12_bins)
                
                song_data_36_bins = {
                    "hpcp": np.array(hpcp_36_bins),
                    "label": str("W_"+original_song_ID),
                    "track_id": str("P_"+original_song_ID)
                }
                self.dataset_36_bins.add_data(song_data_36_bins["track_id"], song_data_36_bins)
                
                song_data_extended = {
                    "hpcp_12_bins": np.array(hpcp_12_bins),
                    "hpcp_36_bins": np.array(hpcp_36_bins),
                    "label": str("W_"+original_song_ID),
                    "track_id": str("P_"+original_song_ID),
                    "audio_features": {
                        "audio_file": str(original_song.split('/')[-1]),
                        "sample_rate": np.float64(sample_rate),
                        "number_channels": np.int32(number_channels),
                        "md5": str(md5),
                        "bit_rate": np.int32(bit_rate),
                        "codec": str(codec)
                    },
                    "hpcp_features": {
                        "frame_size": np.int32(frame_size),
                        "hop_size": np.int32(hop_size),
                        "min_frequency": np.float64(min_frequency),
                        "max_frequency": np.float64(max_frequency),
                        "extraction_time_12_bins": np.float64(extraction_time_12_bins),
                        "extraction_time_36_bins": np.float64(extraction_time_36_bins)
                    },
                    "second_hand_song_API_features": {
                        "title": str(original_song_title),
                        "performer": str(original_song_performer),
                        "url": str(original_song_url),
                        "is_original": np.bool_(original_song_is_original)
                    }
                }
                self.dataset_extended.add_data(song_data_extended["track_id"], song_data_extended)
                
                original_song_folder_path = f"{base_path}/{original_song.split('/')[0]}/"
                files = os.listdir(original_song_folder_path)
                for cover in files:
                    if cover != f"{original_song.split('/')[1]}.mp3":
                        print(f"Cover song: {cover}")
                        # Get cover_song path
                        cover_song_path = original_song_folder_path+cover
                        hpcp_12_bins, hpcp_36_bins, extraction_time_12_bins, extraction_time_36_bins, sample_rate, frame_size, hop_size, min_frequency, max_frequency, number_channels, md5, bit_rate, codec = self.feature_extractor.extract_HPCPs(cover_song_path, resample_quality=0)
                
                        cover_song_title, cover_song_performer, cover_song_url, cover_song_is_original, cover_song_ID = self.get_song_info(cover_song_path)
                        
                        song_data_12_bins = {
                            "hpcp": np.array(hpcp_12_bins),
                            "label": str("W_"+original_song_ID),
                            "track_id": str("P_"+cover_song_ID)
                        }
                        self.dataset_12_bins.add_data(song_data_12_bins["track_id"], song_data_12_bins)
                        
                        song_data_36_bins = {
                            "hpcp": np.array(hpcp_36_bins),
                            "label": str("W_"+original_song_ID),
                            "track_id": str("P_"+cover_song_ID)
                        }
                        self.dataset_36_bins.add_data(song_data_36_bins["track_id"], song_data_36_bins)
                        
                        song_data_extended = {
                            "hpcp_12_bins": np.array(hpcp_12_bins),
                            "hpcp_36_bins": np.array(hpcp_36_bins),
                            "label": str("W_"+original_song_ID),
                            "track_id": str("P_"+cover_song_ID),
                            "audio_features": {
                                "audio_file": str(cover.split('.')[0]),
                                "sample_rate": np.float64(sample_rate),
                                "number_channels": np.int32(number_channels),
                                "md5": str(md5),
                                "bit_rate": np.int32(bit_rate),
                                "codec": str(codec)
                            },
                            "hpcp_features": {
                                "frame_size": np.int32(frame_size),
                                "hop_size": np.int32(hop_size),
                                "min_frequency": np.float64(min_frequency),
                                "max_frequency": np.float64(max_frequency),
                                "extraction_time_12_bins": np.float64(extraction_time_12_bins),
                                "extraction_time_36_bins": np.float64(extraction_time_36_bins)
                            },
                            "second_hand_song_API_features": {
                                "title": str(cover_song_title),
                                "performer": str(cover_song_performer),
                                "url": str(cover_song_url),
                                "is_original": np.bool_(cover_song_is_original)
                            }
                        }
                        self.dataset_extended.add_data(song_data_extended["track_id"], song_data_extended)
                
            
        elif isinstance(self.feature_extractor, CREMAExtractor):
            crema = self.feature_extractor.extract_CREMAs(original_song, resample_quality=0)
            
            original_song_ID = self.get_song_info(original_song_path)
            song_data = {
                "crema": np.array(crema),
                "label": str("P_".join(original_song_ID)),
                "track_id": str("W_".join(original_song_ID))
            }
            self.dataset.add_data(song_data["track_id"], song_data)
                
            return self.dataset
                
        else:
            raise ValueError("Unsupported feature extractor type")
                 
        return self.dataset_12_bins, self.dataset_36_bins, self.dataset_extended
        
            
    def get_song_info(self, song_path):
        # Extract information from the query song file name
        file_name_parts = song_path.split('+')
        
        artist_name = file_name_parts[0].split('/')[-1].replace('_', ' ').title()
        song_name = file_name_parts[2].split('-')[1].split('.')[0].replace('_s_', "'s_").replace('Don_t', "Don't").replace('Can_t', "Can't").replace('_', ' ').title()
        results = self.secondHandSongAPI.search_performance(song_name, artist_name)
        time.sleep(7)
        if results:
            #total_results = results.get("totalResults", 0)
            if results.get("totalResults", 0) == 0:
                title = "title_not_found"
                performer = "performer_not_found"
                url = "uri_not_found"
                is_original = False
                song_ID = "ID_not_found"
                return title, performer, url, is_original, song_ID
            else:
                #total_results = results.get("totalResults", 0)
                #print("Total performances found:", total_results)
                result_page = results.get("resultPage", [])
                for performance in result_page:
                    title = performance.get("title")
                    performer = performance.get("performer", {}).get("name")
                    url = performance.get("uri")
                    is_original = performance.get("isOriginal")
                    song_ID = self.secondHandSongAPI.extract_id(performance.get("uri"))
                    return title, performer, url, is_original, song_ID
        else:
            print("No performances were found for the title '{}' performed by '{}'".format(song_name, artist_name))
            return None