import pandas as pd
import json

class DataStruct:
    """ This module refers to data organization after extracting from Spotify API:
        - These data are stored in a json file
        - We can run this json file and get just values important for us
        - Finally, we will be able to structure these data in pandas DataFrame before loading it in some database
    """
    def __init__(self, filename: str = 'MyTopItems.json') -> None:
        """ Structuring data collection 

        :param: filename (str): was set as "MyTopItems.json" if a specific name doesn't specified
        """
        self.filename = filename

    def struct_top_items(self) -> object:

        song_names = []
        song_id = []
        artist_names = []
        album_name = []
        release_date = []
        popularity = []

        with open(self.filename) as json_file:
            mydata = json.load(json_file)

        ### Storing our data into lists
        for song in mydata['items']:
            song_names.append(song['name'])
            song_id.append(song['id'])
            artist_names.append(song['artists'][0]['name'])
            album_name.append(song['album']['name'])
            release_date.append(song['album']['release_date'])
            popularity.append(song['popularity'])

        ### Dictionary to structure our data before transforming in pandas DataFrame
        song_dict = {
            'song_id': song_id,
            'song': song_names,
            'artist': artist_names,
            'album': album_name,
            'release': release_date,
            'popularity': popularity
        }

        ### Here we could structured our data in pandas and returned as a object
        df = pd.DataFrame(song_dict, columns=['song_id', 'song', 'artist', 'album', 'release', 'popularity'])
        return df
    
    def get_tracks_uris(self) -> list:
        """Get uris from json file
        
        :filename (str): json file name
        :return (uris): uris Spotify tracks list
        """
        uris = []
        with open(self.filename) as json_file:
            mydata = json.load(json_file)

        for song in mydata['items']:
            uris.append(song['uri'])
            
        return uris
    