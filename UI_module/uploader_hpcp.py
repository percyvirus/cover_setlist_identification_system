import sys 
import os
import essentia.standard as estd

sys.path.append(os.getcwd())
from domain_model import *

class Uploader_hpcp:
    def __init__(self):
        pass
        
    def upload_hpcp(client, database_name, collection_name, hpcp, label, track_id):
        try:
            # Select database
            db = client[database_name]
            
            # Select collection
            db_collection = db[collection_name]
            
            # Construct the document
            document = {
                "hpcp": hpcp,  # Convertir ndarray a lista
                "label": str(label),
                "track_id": str(track_id)
            }
            
            # Insert document to collection
            result = db_collection.insert_one(document)
            
            # Verify insertion
            if result.inserted_id:
                print("Document inserted successfully:", result.inserted_id)
            else:
                print("Error inserting the document")

        except Exception as e:
            self.ui.display_error(f"Error loading audio file: {str(e)}")
            return None
        

