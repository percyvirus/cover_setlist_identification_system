import sys 
import os
import re
import json

from UI_module.UI import UI
from algorithms import *
from domain_model.dataset import Dataset
from domain_model.featureExtractor import FeatureExtractor
from domain_model.datasetCreator import DatasetCreator
from domain_model.datasetLoader import DatasetLoader
from domain_model.datasetSaver import DatasetSaver
from domain_model.exiter import Exiter
from domain_model.statisticalExtractor import StatisticalExtractor
from domain_model.database import Database
# from UI_module.creator import Creator
# from UI_module.loader_audio import Loader_audio
# from UI_module.uploader_hpcp import Uploader_hpcp
from domain_model.second_hand_song_API import SecondHandSongsAPI
# from UI_module.saver import Saver
sys.path.append(os.getcwd())
from domain_model import *
# from usecasesmarker import *

# from entities.circular_dependency_exception import CircularDependencyException
with open('config.json') as f:
            config = json.load(f)
            
collection = "Covers80_HPCP"

class Controller:
    def __init__(self):
        self.ui = UI(self)
        self.algorithm = None
        self.datasets = {}
        self.featureExtractor = None
        self.datasetCreator = None
        # self.datasetLoader = DatasetLoader()
        self.datasetSaver = DatasetSaver(self)
        # self.exiter = Exiter(self.ui)
        # self.statisticalExtractor = StatisticalExtractor()
        self.secondHandSongAPI = SecondHandSongsAPI()
        
        # Read configuration from JSON file
        with open('config.json') as f:
            config = json.load(f)
        self.uri = config['uri']
        self.database_name = config['database']
        self.database = Database(self.uri, self.database_name)
        
        # self.loader_audio = Loader_audio()
        # self.uploader_hpcp = Uploader_hpcp()


    def run(self):
        while True:
            try:
                self.ui.display_menu()
                self.ui.handle_user_input()
            except:
                print("An exception occurred")
            
    def execute_Qmax(self, file_path):
        pass
        
    def create_dataset(self, list_original_songs, feature_extractor_type, dataset_name):
        if feature_extractor_type == "HPCP":
            dataset_hpcp_12_bins = Dataset()
            dataset_hpcp_36_bins = Dataset()
            dataset_hpcp_extended = Dataset()
            
            dataset_name_HPCP_12_bins = f"{dataset_name}_HPCP_12_bins"
            dataset_name_HPCP_36_bins = f"{dataset_name}_HPCP_36_bins"
            dataset_name_HPCP_extended = f"{dataset_name}_extended"
            
            self.datasetCreator = DatasetCreator(self, feature_extractor_type)
            dataset_hpcp_12_bins, dataset_hpcp_36_bins, dataset_hpcp_extended = self.datasetCreator.create_dataset(list_original_songs)
            
            self.datasets[dataset_name_HPCP_12_bins] = dataset_hpcp_12_bins
            self.datasets[dataset_name_HPCP_36_bins] = dataset_hpcp_36_bins
            self.datasets[dataset_name_HPCP_extended] = dataset_hpcp_extended
            
        elif feature_extractor_type == "CREMA":
            dataset_crema = Dataset()
        
            self.datasetCreator = DatasetCreator(self, feature_extractor_type)
            dataset_crema = self.datasetCreator.create_dataset(list_original_songs)
            
            self.datasets[dataset_name] = dataset_crema 
            

    def display_datasets(self):
        print("\nAvailable datasets:")
        for i, dataset_name in enumerate(self.datasets.keys(), 1):
            print(f"{i}. {dataset_name}")
        
        print()
        print("Press enter to continue...")
        input()  # Wait for the user to press Enter

    
    def save_datasets(self):
        self.datasetSaver.save_dataset("dataset_name", save_locally=True, save_to_mongodb=False)
    
    def save_all_datasets(self, save_locally=True, save_to_mongodb=False):
        for dataset in self.datasets.items():
            self.datasetSaver.save_dataset(dataset, save_locally, save_to_mongodb)
        

    