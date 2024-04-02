import sys 
import os
import essentia.standard as estd

sys.path.append(os.getcwd())
from domain_model import *

class Loader_audio:
    def __init__(self):
        pass
        
    def load_audio_file(self, file_path):
        try:
            audio = estd.AudioLoader(filename=file_path)()
        except Exception as e:
            self.ui.display_error(f"Error loading audio file: {str(e)}")
            return None
        
        return audio

