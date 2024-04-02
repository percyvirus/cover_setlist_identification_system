class Dataset:
    def __init__(self):
        self.data = {}

    def add_data(self, track_id, data):
        if track_id in self.data:
            self.data[track_id].append(data)
        else:
            self.data[track_id] = [data]

    def get_data(self, track_id):
        return self.data.get(track_id)

    def iterate_data(self):
        for track_id, data_list in self.data.items():
            for data in data_list:
                yield track_id, data
