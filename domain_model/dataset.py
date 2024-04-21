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
    
    def _is_original_song(self, data):
        if "label" in data and "track_id" in data:
            label_id = data["label"].split("_")[1]
            track_id_id = data["track_id"].split("_")[1]
            return label_id == track_id_id
        return False

    def iterate_original_songs_data(self):
        for track_id, data_list in self.data.items():
            for data in data_list:
                if self._is_original_song(data):
                    label_id = data["label"]
                    original_song_track_id = data["track_id"]
                    yield label_id, original_song_track_id, data
                        
    def iterate_cover_songs_data(self):
        for track_id, data_list in self.data.items():
            for data in data_list:
                if not self._is_original_song(data):
                    yield track_id, data
    
    def count_original_songs(self):
        count = 0
        for track_id, data_list in self.data.items():
            for data in data_list:
                if "label" in data and "track_id" in data:
                    label_id = data["label"].split("_")[1]
                    track_id_id = data["track_id"].split("_")[1]
                    if label_id == track_id_id:
                        count += 1
        return count

    def count_cover_songs(self):
        count = 0
        for track_id, data_list in self.data.items():
            for data in data_list:
                if "label" in data and "track_id" in data:
                    label_id = data["label"].split("_")[1]
                    track_id_id = data["track_id"].split("_")[1]
                    if label_id != track_id_id:
                        count += 1
        return count