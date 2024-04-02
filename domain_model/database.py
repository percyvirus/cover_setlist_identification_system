from pymongo import MongoClient

class Database:
    def __init__(self, connection_string, database_name, collection_name=None):
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.collection = None

    def set_collection(self, collection_name):
        self.collection_name = collection_name
        self.collection = self.db[collection_name]

    def insert_dataset(self, dataset):
        if not self.collection:
            raise ValueError("Collection has not been defined. Use set_collection() to define it first.")
        self.collection.insert_one({"data": dataset.data})

    def get_datasets(self):
        if not self.collection:
            raise ValueError("Collection has not been defined. Use set_collection() to define it first.")
        datasets = []
        for item in self.collection.find():
            datasets.append(Dataset(item["data"]))
        return datasets