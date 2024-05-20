class Dataset:
    def __init__(self):
        self.data = {}
        self.count_not_ID = 0

    def add_data(self, track_id, data):
        """if track_id == 'P_performance_ID_not_found':
            if track_id in self.data:
                self.data[track_id].append(data)
            else:
                self.data[track_id] = [data] 
        el"""
        if track_id in self.data:
            self.data[track_id].append(data)
        else:
            self.data[track_id] = data

    def get_data(self, track_id):
        return self.data.get(track_id)

    def iterate_data(self):
        for track_id, data_list in self.data.items():
            for data in data_list:
                yield track_id, data
    
    def is_original_song(self, data):
        if data['second_hand_song_API_features']['is_original']:
            label_id = data["label"].split("_")[1]
            track_id_id = data["track_id"].split("_")[1]
            return label_id == track_id_id
        return False

    def iterate_original_songs_data(self):
        for key, performance in self.data.items():
            if performance['second_hand_song_API_features']['is_original']:
                label_id = performance["label"]
                #original_song_track_id = performance["track_id"]
                yield label_id, key, performance
            #if data['label']['track_id']:
            #    return True
                        
    def iterate_cover_songs_data(self):
        for key, performance in self.data.items():
            """if key == 'P_performance_ID_not_found':
                if not performance[self.count_not_ID]['second_hand_song_API_features']['is_original']:
                    self.count_not_ID = self.count_not_ID + 1
                    yield key, performance[self.count_not_ID-1]
            el"""
            if not performance['second_hand_song_API_features']['is_original']:
                yield key, performance
    
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