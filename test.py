from pymongo import MongoClient
from pymongo.server_api import ServerApi
import numpy as np
import math
# Connection String: mongodb+srv://percy:<password>@percy.pizmcnl.mongodb.net/

import matplotlib.pyplot as plt

sample_rate = 16000
frame_size = sample_rate * 0.1
frame_size = int(2 ** math.ceil(math.log2(frame_size)))
hop_size=int(frame_size/2)
frame_time = frame_size/sample_rate
hop_time = hop_size/sample_rate
min_frequency=50
max_frequency=5000

confusion_matrix = [['Qmax_12_bins', 'sine_220_Hz', 'sine_224,28_Hz', 'sine_440_Hz', 'sine_233,08_Hz', 'sine_110_Hz'],
                    ['sine_220_Hz', 0.10204081982374191, 0.10810811072587967, 0.10638298094272614, 0.10204081982374191, 0.10869564861059189],
                    ['sine_224,28_Hz', 0.11049723625183105, 0.10204081982374191, 0.10869564861059189, 0.10204081982374191, 0.10869564861059189],
                    ['sine_440_Hz', 0.10869564861059189, 0.11235955357551575, 0.10204081982374191, 0.10204081982374191, 0.10928961634635925],
                    ['sine_233,08_Hz', float('inf'), float('inf'), float('inf'), 0.10204081982374191, float('inf')],
                    ['sine_110_Hz', 0.10989011079072952, 0.11049723625183105, 0.10638298094272614, 0.10204081982374191, 0.10204081982374191]]

confusion_array = np.array(confusion_matrix)

confusion_array[1:, 1:][confusion_array[1:, 1:] == 'inf'] = 1
# Obtener etiquetas y valores de la matriz
labels = confusion_array[0, 1:]
values = confusion_array[1:, 1:].astype(float)

# Plotear la matriz de confusión
plt.figure(figsize=(11, 8))
plt.imshow(values, cmap='cool')

# Añadir las etiquetas de los ejes
plt.xticks(ticks=range(len(labels)), labels=labels, rotation=45)
plt.yticks(ticks=range(len(labels)), labels=labels)
plt.xlabel('Signal 2')
plt.ylabel('Signal 1')
plt.title('Confusion Matrix')

# Añadir los valores en cada celda
for i in range(len(labels)):
    for j in range(len(labels)):
        plt.text(j, i, format(values[i][j], '.6f'),
                 horizontalalignment='center',
                 color='white' if values[i][j] > 0.5 else 'black')

plt.colorbar(label='Accuracy')
plt.tight_layout()
plt.show()


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
    

