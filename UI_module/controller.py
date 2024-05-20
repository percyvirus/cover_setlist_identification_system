import sys 
import os
import re
import json
import deepdish as dd

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
from algorithms.qmax import Qmax
from algorithms.qmax_and_qmax_bis import Qmax_and_Qmax_bis
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
        self.running = True
        self.datasets = {}
        self.ui = UI(self, self.datasets)
        self.algorithm = None
        self.featureExtractor = None
        self.datasetCreator = None
        self.datasetLoader = DatasetLoader(self)
        self.datasetSaver = DatasetSaver(self)
        # self.exiter = Exiter(self.ui)
        # self.statisticalExtractor = StatisticalExtractor()
        self.secondHandSongAPI = SecondHandSongsAPI()
        self.statistical_extractor = StatisticalExtractor()
        
        # Read configuration from JSON file
        with open('config.json') as f:
            config = json.load(f)
        self.uri = config['uri']
        self.database_name = config['database']
        self.database = Database(self.uri, self.database_name)
        
        # self.loader_audio = Loader_audio()
        # self.uploader_hpcp = Uploader_hpcp()


    def run(self):
        while self.running:
            try:
                self.ui.display_menu()
                self.ui.handle_user_input()
            except:
                print("An exception occurred")
            
        
    def create_dataset(self, list_original_songs, feature_extractor_type, dataset_name):
        if feature_extractor_type == "HPCP":
            dataset_hpcp_12_bins = Dataset()
            dataset_hpcp_36_bins = Dataset()
            dataset_hpcp_extended = Dataset()
            
            dataset_name_HPCP_12_bins = f"{dataset_name}_HPCP_12_bins"
            dataset_name_HPCP_36_bins = f"{dataset_name}_HPCP_36_bins"
            dataset_name_HPCP_extended = f"{dataset_name}_extended"
            
            self.datasetCreator = DatasetCreator(self, feature_extractor_type)
            dataset_hpcp_12_bins, dataset_hpcp_36_bins, dataset_hpcp_extended, failed_original_performances_list, failed_cover_performances_list, original_performances_that_are_not_original_performance_list, cover_performances_that_are_not_cover_performance_list = self.datasetCreator.create_dataset(list_original_songs)
            
            dd.io.save(f"{dataset_name}_dataset.h5", {
                'dataset_hpcp_12_bins': dataset_hpcp_12_bins,
                'dataset_hpcp_36_bins': dataset_hpcp_36_bins,
                'dataset_hpcp_extended': dataset_hpcp_extended,
                'failed_original_performances_list': failed_original_performances_list,
                'failed_cover_performances_list': failed_cover_performances_list,
                'original_performances_that_are_not_original_performance_list': original_performances_that_are_not_original_performance_list,
                'cover_performances_that_are_not_cover_performance_list': cover_performances_that_are_not_cover_performance_list
            })
            
            print(f"Backup saved at: {dataset_name}_dataset.h5")
            
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

    def load_datasets(self, file_path): #DONE
        self.datasetLoader.load_dataset_locally(file_path, save_locally=True, save_to_mongodb=False)
    
    def save_datasets(self):    # TODO: IMPLEMENT
        self.datasetSaver.save_dataset("dataset_name", load_locally=True, load_from_mongodb=False)
        
    def execute_qmax(self, dataset, results_path):    # TODO: IMPLEMENT
        self.algorithm = Qmax_and_Qmax_bis(True)
        self.algorithm.execute_qmax_bis(dataset, results_path)
        
    def execute_qmax_bis(self, dataset, results_path):    # TODO: IMPLEMENT
        self.algorithm = Qmax_and_Qmax_bis(False)
        self.algorithm.execute_qmax_bis(dataset, results_path)
        
    def get_statistics(self, confusion_matrix_path):    # TODO: IMPLEMENT
        self.statistical_extractor.calculate_metrics(confusion_matrix_path)
    
    def save_all_datasets(self, save_locally=True, save_to_mongodb=False):  #DONE
        for dataset in self.datasets.items():
            self.datasetSaver.save_dataset(dataset, save_locally, save_to_mongodb)
    
    def execute_Qmax_bis_with_COVERS80(self):
        dataset_path = './DATASETS/CUVERS80_extended'
        results_dataset_path = './DATASETS/CUVERS80_extended/RESULTS'
        self.load_datasets(dataset_path)
        self.execute_qmax_bis(self.datasets['CUVERS80_extended'], results_dataset_path)
    
    def exit_program(self):
        self.running = False
        

    