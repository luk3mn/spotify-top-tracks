import requests

class GetData:
    """ This module refers to extract data from your source
        - We used Spotify API to get my private data from top itens in my spotify account

    """
    def __init__(self, api_url) -> None:
        self.api_url = api_url

    def get_user_top_items(self, limit: int, headers: object, type: str, offset: int=0, time_range: str = 'medium_term', filename: str = 'MyTopItems.json') -> object:
        """ Used to request our data on Spotify API
            - filename: it was set as 'MyTopItems.json' in cause nothing are specified on module callable
            - time_range: there are three option based on API instructions, they are shor_term (about 4 weeks), medium_term (approximately last 6 months) and long_term (calculated from several years of data and including all new data as it becomes available)
        """
        response = requests.get(url=f'{self.api_url}me/top/{type}?limit={limit}&offset={offset}&time_range={time_range}', headers=headers)

        ### write a json file ith our collection data
        with open(filename, 'w') as f:
            f.write(response.text)
            
        return response.json() # return json with the response
