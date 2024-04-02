from pymongo import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
# Connection String: mongodb+srv://percy:<password>@percy.pizmcnl.mongodb.net/

uri = "mongodb+srv://percy:percy@percy.pizmcnl.mongodb.net/?retryWrites=true&w=majority&appName=Percy"
database = "Percy"
collection = "Covers80_HPCP"

def insert_document(client, database_name, collection_name, hpcp, label, track_id): 
    # Create a new client and connect to the server
    client = MongoClient(uri)

    # Select database
    db = client[database]

    # Select collection
    db_collection = db[collection]

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        print(f"Database: {db.name}")
        print(f"Availables collections:")
        for collection_name in db.list_collection_names():
            print(collection_name)
        print(f"Collection used: {db_collection.name}")
    except Exception as e:
        print(e)
        
    document = {
        "hpcp": np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]).tolist(),  # Convertir ndarray a lista
        "label": np.str_("etiqueta"),
        "track_id": np.str_("ID_de_pista")
    }

    # Insert document to collection
    result = db_collection.insert_one(document)

    # Verify insertion
    if result.inserted_id:
        print("Document inserted succesfully:", result.inserted_id)
    else:
        print("Error inserting the document")
    

