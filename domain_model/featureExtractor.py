from abc import ABC, abstractmethod
class FeatureExtractor(ABC):
    
    def __init__(self):
        pass

    @abstractmethod
    def extract_features(self):
        pass


