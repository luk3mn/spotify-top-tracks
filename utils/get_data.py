import requests


class GetData:
    """To be able to extract private data from Spotify Account"""

    def __init__(self, endpoint: str, headers: object, filename: str = 'MyTopItems.json') -> object:
        """
        :param endpoint (str): specify the endpoint that it will be used
        :param headers (object): to set the headers that it will be used
        :param filename (str): it was set as 'MyTopItems.json' in cause nothing are specified on module callable
        """
        self.__endpoint = endpoint
        self.__headers = headers
        self.__filename = filename

    def get_users_top_items(self, limit: int = 20, offset: int = 0, type: str = 'tracks', time_range: str = 'medium_term') -> object:
        """Get user's top items of the type 'tracks' from Spotify API

        :param limit (int): The maximum number of items to return. Default: 20. Minimum: 1. Maximum: 50
        :param offset (int): The index of the first item to return. Default: 0 (the first item). Use with limit to get the next set of items.
        :param type (int): The type of entity to return, artists or tracks. Default: 'tracks'
        :param time_range: there are three option based on API instructions, they are short_term (about 4 weeks), medium_term (approximately last 6 months) and long_term (calculated from several years of data and including all new data as it becomes available)
        :return response (json): json response 
        """
        response = requests.get(
            url=f'{self.__endpoint}me/top/{type}?limit={limit}&offset={offset}&time_range={time_range}', headers=self.__headers)

        ### write a json file ith our collection data
        with open(self.__filename, 'w') as f:
            f.write(response.text)

        return response.json()
