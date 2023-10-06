import pandas as pd
import json

class DataStruct:
    """ This module refers to data organization after extracting from Spotify API:
        - These datas are stored in a json file
        - We can run this json file and get just values important for us
        - Finally, we will be able to structure these data in pandas dataframe before loading it in some database
    """
    def __init__(self) -> None:
        self.__mydata = ''
        self.__song_dict = {}
        self.__song_names = []
        self.__song_id = []
        self.__artist_names = []
        self.__album_name = []
        self.__release_date = []
        self.__popularity = []

    """ Structuring data collecton """
    def struct_top_items(self, filename: str = 'MyTopItems.json') -> object:
        """ filename was set as "MyTopItems.json" if a espefic name doesn't especified
        """
        with open(filename) as json_file:
            self.__mydata = json.load(json_file)

        ### Storing our data into lists
        for song in self.__mydata['items']:
            self.__song_names.append(song['name'])
            self.__song_id.append(song['id'])
            self.__artist_names.append(song['artists'][0]['name'])
            self.__album_name.append(song['album']['name'])
            self.__release_date.append(song['album']['release_date'])
            self.__popularity.append(song['popularity'])

        ### Dictionary to structure our data before transforming in pandas dataframe
        self.__song_dict = {
            'song_id': self.__song_id,
            'song': self.__song_names,
            'artist': self.__artist_names,
            'album': self.__album_name,
            'release': self.__release_date,
            'popularity': self.__popularity
        }

        ### Here we could structured our data in pandas and returned as a objetc
        df = pd.DataFrame(self.__song_dict, columns=['song_id', 'song', 'artist', 'album', 'release', 'popularity'])
        return df
        